from flask import *
import os
from helper import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/NPR')
def NPR():
    return render_template('number_plate.html')

@app.route('/NPRImage')
def NPRImage():
    return render_template('number_plate_image.html')

@app.route('/extract_text',methods=["POST"])
def extract_text():
    file=request.files['file']
    folder_path = "static\Temporary Storage"
    file_path = os.path.join(folder_path, file.filename)
    # print(file_path)
    file.save(file_path)  
    extracted_text=number_plate_from_image(file_path)
    os.remove(file_path)
    # print(extract_text)
    return extracted_text

@app.route('/NPRVideo')
def NPRVideo():
    return render_template('number_plate_video.html')

@app.route('/NPRVideoLoad')
def NPRVideoLoad():
    return Response(NPR_gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/display_plates',methods=['POST'])
def display_plates():
    plates=[]
    folder_path = r"static\Temporary Storage"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        k = number_plate_from_image(file_path)
        if k not in plates:
            plates.append(k)
        os.remove(file_path)
    return render_template('number_plates_list.html',k=plates)

@app.route('/object')
def object():
    return render_template('object_detection.html')

@app.route('/ObjImage')
def ObjImage():
    return render_template('object_detection_image.html')

@app.route('/detect_objects',methods=["GET","POST"])
def detect_objects():
    file=request.files['file']
    folder_path = "static/Temporary Storage"
    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)  
    processed_image = objects_from_image(file_path)
    os.remove(file_path)
    return jsonify({'processed_image_url': processed_image})

@app.route('/ObjVideo')
def ObjVideo():
    return render_template('object_detection_video.html')

@app.route('/ObjVideoLoad')
def ObjVideoLoad():
    return Response(Obj_gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.run(debug=True)