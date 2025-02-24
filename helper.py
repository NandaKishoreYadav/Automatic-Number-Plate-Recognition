import cv2
import pytesseract
from ultralytics import YOLO
from random import randint

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'

def number_plate_from_image(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    number_plate_contours = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)
        if aspect_ratio > 2.0 and aspect_ratio < 5.0 and area > 1000:
            number_plate_contours.append(contour)
    for contour in number_plate_contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        roi = blurred[y:y+h, x:x+w]
        number_plate_text = pytesseract.image_to_string(roi, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -l eng')
        return number_plate_text
    return ''

def NPR_gen_frames():
    cap=cv2.VideoCapture(0)
    harcascade = "Haarcascades/haarcascade_russian_plate_number.xml"
    cap.set(3, 640) # width
    cap.set(4, 480) #height
    min_area = 500
    count = 0
    num=0
    while True:
        success, img = cap.read()  # read the camera frame
        if not success:
            break
        else:
            plate_cascade = cv2.CascadeClassifier(harcascade)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

            for (x,y,w,h) in plates:
                area = w * h

                if area > min_area:
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    
                    img_roi = img[y: y+h, x:x+w]
                    cv2.imwrite("static/Temporary Storage/number_plate_{}.jpg".format(num), img_roi)
                    num+=1
            
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def objects_from_image(img):
    model = YOLO('yolo model/yolov8x.pt')
    results = model(img, show=False)
    if isinstance(results, list):
        for i, img_result in enumerate(results):
            output_path = "static/processed_image.jpg"
            img_result.save(output_path)
    return output_path

def Obj_gen_frames():
    dnn = cv2.dnn.readNet('yolo model/yolov4-tiny.weights', 'yolo model/yolov4-tiny.cfg')
    model = cv2.dnn_DetectionModel(dnn)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
    with open('yolo model/classes.txt') as f:
        classes = f.read().strip().splitlines()
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    color_map = {}
    while True:
        success, img = capture.read()  # read the camera frame
        frame = img.copy()  # Make a copy of the original frame
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        if not success:
            break
        else:
            try:
                class_ids, confidences, boxes = model.detect(frame)
                for id, confidence, box in zip(class_ids, confidences, boxes):
                    x, y, w, h = box
                    obj_class = classes[id]

                    if obj_class not in color_map:
                        color = (randint(0, 255), randint(0, 255), randint(0, 255))
                        color_map[obj_class] = color
                    else:
                        color = color_map[obj_class]

                    cv2.putText(frame, f'{obj_class.title()} {format(confidence, ".2f")}', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            except Exception as e:
                print("Error during detection:", e)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
