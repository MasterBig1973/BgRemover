import os
import shutil
from rembg import remove
from PIL import Image
import io
import cv2
import torch
import concurrent.futures
from moviepy.editor import VideoFileClip  # Не забудьте импортировать для обработки видео

# Проверка доступности GPU
print(f"PyTorch видит GPU: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Имя GPU: {torch.cuda.get_device_name(0)}")
    print(f"Текущий девайс: {torch.cuda.current_device()}")
else:
    print("GPU не доступен, работает на CPU")

# Папки для работы
input_folder = 'INPUT-VIDEO'
output_folder = 'OUTPUT-VIDEO'
frame_folder = 'FRAME'
background_image_path = 'image.jpg'  # Путь к картинке фона
background_color = (0, 255, 0, 255)  # По умолчанию зеленый цвет фона (RGBA)

# Очистка только выходных папок
for folder in [output_folder, frame_folder]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

# Функция для загрузки фона (если изображение задано)
def load_background():
    if os.path.exists(background_image_path):
        print(f"Загружаем фон из {background_image_path}")
        return Image.open(background_image_path).convert("RGBA")
    else:
        print("Используется фон по умолчанию (зеленый)")
        return None

# Функция для обработки одного видео
def process_video(file_name):
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_processed.mp4')

    if os.path.exists(output_path):
        print(f"Файл {file_name} уже обработан, пропускаем.")
        return

    print(f"Открываем видео: {input_path}")
    video = cv2.VideoCapture(input_path)
    if not video.isOpened():
        print(f"Ошибка: Не удалось открыть видео {file_name}")
        return

    fps = 25
    frame_count = 0
    background = load_background()  # Загружаем фон при старте

    print("Извлекаем и обрабатываем кадры...")
    while True:
        success, frame = video.read()
        if not success:
            break

        # Отображаем текущую загрузку GPU
        if torch.cuda.is_available():
            print(f"Загрузка GPU перед обработкой кадра {frame_count}: {torch.cuda.memory_allocated(0) / 1e6} MB")

        # Конверсия кадра
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        frame_data = buffer.getvalue()

        # Удаление фона на GPU или CPU в зависимости от доступности GPU
        if torch.cuda.is_available():
            torch.cuda.synchronize()  # Синхронизация для точного замера
            print(f"Кадр {frame_count}: Начинаем обработку на GPU...")
            output_data = remove(frame_data, provider="cuda")  # Использование GPU
        else:
            print(f"Кадр {frame_count}: Начинаем обработку на CPU...")
            output_data = remove(frame_data, provider="cpu")  # Использование CPU

        # Конвертация результата
        image = Image.open(io.BytesIO(output_data))

        # Если фон задан как изображение
        if background:
            background_resized = background.resize(image.size)
            background_resized.paste(image, (0, 0), image)
            image = background_resized
        else:
            # Если фон задан как цвет
            green_background = Image.new('RGBA', image.size, background_color)
            green_background.paste(image, (0, 0), image)
            image = green_background

        # Сохранение кадра
        frame_path = os.path.join(frame_folder, f"frame_{frame_count:06d}.png")
        image.save(frame_path, 'PNG')
        frame_count += 1
        if frame_count % 100 == 0:
            print(f"Обработано {frame_count} кадров")

        # Отображаем текущую загрузку GPU после обработки
        if torch.cuda.is_available():
            print(f"Загрузка GPU после обработки кадра {frame_count}: {torch.cuda.memory_allocated(0) / 1e6} MB")

    video.release()
    print(f"Извлечено и обработано {frame_count} кадров из {file_name}")

    # Собираем видео
    frame_files = sorted(os.listdir(frame_folder))
    if not frame_files:
        print(f"Ошибка: Нет кадров для сборки видео из {file_name}")
        return

    print("Собираем видео из кадров...")
    first_frame = cv2.imread(os.path.join(frame_folder, frame_files[0]))
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_video_path = os.path.join(output_folder, "temp_video.mp4")
    video_writer = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

    for frame_file in frame_files:
        frame_path = os.path.join(frame_folder, frame_file)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

    video_writer.release()
    print(f"Видео без звука собрано: {temp_video_path}")

    print("Добавляем аудио...")
    # Далее обработка звука и финальная сборка
    original_video = VideoFileClip(input_path)
    processed_video = VideoFileClip(temp_video_path)
    final_video = processed_video.set_audio(original_video.audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Готовое видео с аудио сохранено: {output_path}")

    os.remove(temp_video_path)

# Обработка видео с многозадачностью
def process_all_videos():
    video_files = [file_name for file_name in os.listdir(input_folder) if file_name.lower().endswith(('.mp4', '.avi', '.mov'))]
    print(f"Найдено видео файлов: {len(video_files)}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Запуск параллельной обработки для каждого файла
        executor.map(process_video, video_files)

# Запуск обработки всех видео
process_all_videos()

print("Обработка всех видео завершена!")
