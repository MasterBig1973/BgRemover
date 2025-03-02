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
