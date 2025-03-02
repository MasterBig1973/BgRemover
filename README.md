This script is designed for automatic video file processing, including background removal from each frame and replacing it with an image or color. Processing can be done using a Graphics Processing Unit (GPU) if available, or using a Central Processing Unit (CPU). It utilizes the rembg library for background removal, cv2 for frame manipulation, PIL for image processing, and moviepy for audio and video handling.

Functionality:

Background Removal:
Each video frame has its background removed using the rembg library. The background can be replaced with a pre-defined image or a solid color.

GPU or CPU Processing:
If a GPU is available, the processing happens on the GPU, which speeds up the process. Otherwise, the CPU is used for processing.

Video Handling:
The video is extracted and split into frames. After background removal, each frame is saved as a separate file. The frames are then reassembled into the final video.

Audio Integration:
After the video is processed, the original audio from the input video is added back to the output video.

Multithreading:
Videos are processed concurrently using ThreadPoolExecutor for efficient handling of multiple videos.

# Installation

To install the project dependencies, follow these steps:

1. Make sure you have Python version 3.10 installed. The project has only been tested on this version.
2. Create and activate a virtual environment:
 
 ```bash
   python -m venv venv
   # Для Windows:
   .\venv\Scripts\activate
   # Для macOS/Linux:
   source venv/bin/activate
   
Update pip to the latest version:

3. python -m pip install --upgrade pip

Install dependencies with the following command:  

4. pip install -r requirements.txt -f https://download.pytorch.org/whl/cu121/torch_stable.html

This command will install all the libraries required to run the project, including PyTorch with CUDA support.

------------------------------------------------------------------------------------------------------------------

# Changing the Background Color

In this project, the default background color is set to green (RGBA) for video processing. To change the background color, you can do the following:

1. **Default - Green Color**: The green color is set as `(0, 255, 0, 255)`. This means the background will be green with full opacity.

2. **Setting a Transparent Background**: To use a transparent background, change the `background_color` variable to `(0, 0, 0, 0)`. This will create a fully transparent background. You need to ensure that you have a color alpha channel to work with transparency in the image.

   ```python
   background_color = (0, 0, 0, 0)  # Transparent background (RGBA)
Copy
Using a Custom Image as Background: If you want to replace the background with an image, simply specify the path to your image in the background_image_path variable. If the file exists, it will be loaded and used as the background.

background_image_path = 'path/to/your/background_image.jpg'  # Path to the background image
Copy
Example of Modifying Variables in the Code
# Default green background
background_color = (0, 255, 0, 255)  # Green background color

# For a transparent background
# background_color = (0, 0, 0, 0)  # Transparent background

# For a custom background image
# background_image_path = 'image.jpg'  # Path to the background image
Copy
How This Looks in the Code
You can also add comments in the code to make it clearer:

# Setting the default background (green)
background_color = (0, 255, 0, 255)  # Green background color (RGBA)
# To use a transparent background, replace with:
# background_color = (0, 0, 0, 0)  # Transparent background (RGBA)

# Path to the background image
background_image_path = 'image.jpg'  # Replace with the path to your image
