# Automatic Number Plate Recognition

This project implements an Automatic Number Plate Recognition (ANPR) system. It uses Optical Character Recognition (OCR) with `pytesseract`, object detection with the YOLO model, and number plate detection with Haarcascades.

## Features

- **Number Plate Recognition:** Extracts and recognizes the number plate from images or live video feeds.
- **Object Detection:** Detects objects in images or live video feeds.
- **Support for Live Video and Image Upload:** You can process both live video and images by uploading them.

## Installation and Setup

Follow these steps to set up and run the project:

1. Clone the Repository:

   ```bash
   git clone https://github.com/NandaKishoreYadav/Automatic-Number-Plate-Recognition.git
   ```
   
2. Install Tesseract-OCR

-  Download the Tesseract-OCR executable from [this link](https://github.com/UB-Mannheim/tesseract/wiki).
-  Make a note of the path where `tesseract.exe` is installed.

3. Download YOLOv8 Model

-  Download the YOLOv8x model file from [this link](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8x.pt).
-  Place the downloaded `yolov8x.pt` file in the `yolo_model` folder.

4. Open a command prompt from the project directory and create a new virtual environment:
    ```sh
    python -m venv myenv
    ```
5. Activate your environment:
    - On Windows:
        ```sh
        myenv\Scripts\activate
        ```
    - On Linux:
        ```sh
        source myenv/bin/activate
        ```
6. Install the necessary dependencies:
    ```sh
    pip install -r requirements.txt
    ```
7. Run the application:
    ```sh
    python app.py
    ```
## Usage

Once the application is running, you can choose between the following options:

- **Number Plate Recognition:** Process images or live video feeds to extract and recognize number plates.
- **Object Detection:** Detect objects in images or live video feeds.

Upload an image or select the live video feed option to get started.

## Notes

- Ensure that the path to `tesseract.exe` is correctly set in line 6 of helper.py.
- Verify that the YOLO model file is correctly placed in the `yolo_model` folder.

## Contact

If you have any questions or feedback, please feel free to reach out.

Thank you for using Automatic Number Plate Recognition! 😊
