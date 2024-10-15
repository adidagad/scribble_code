'''from flask import Flask, render_template, Response, jsonify
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

# Open the camera
camera = cv2.VideoCapture(0)

def gen_frames():
    """Generate frames from the camera."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def ocr_from_frame(frame):
    """Process the frame for OCR and return the extracted text."""
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image)
    _, binary_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform OCR
    text = pytesseract.image_to_string(binary_image)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream the camera feed."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_ocr', methods=['GET'])
def capture_ocr():
    """Capture the current frame from the camera and perform OCR."""
    success, frame = camera.read()
    if success:
        extracted_text = ocr_from_frame(frame)  # Process frame for OCR
        return jsonify({"extracted_text": extracted_text})
    else:
        return jsonify({"error": "Failed to capture image"}), 500

if __name__ == "__main__":
    app.run(debug=True)'''









import subprocess
from flask import Flask, render_template, Response, jsonify, request
import cv2
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

# Open the camera
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def ocr_from_frame(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image)
    _, binary_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    text = pytesseract.image_to_string(binary_image)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

'''@app.route('/capture_ocr', methods=['GET'])
def capture_ocr():
    success, frame = camera.read()
    if success:
        extracted_text = ocr_from_frame(frame)
        return jsonify({"extracted_text": extracted_text})
    else:
        return jsonify({"error": "Failed to capture image"}), 500'''



@app.route('/capture_ocr', methods=['GET'])
def capture_ocr():
    success, frame = camera.read()  # Capture the frame from the camera
    if success:
        print("Frame captured successfully")
        extracted_text = ocr_from_frame(frame)  # Process the frame for OCR
        print(f"Extracted OCR Text: {extracted_text}")
        return jsonify({"extracted_text": extracted_text})  # Return the text as JSON
    else:
        print("Failed to capture frame")
        return jsonify({"error": "Failed to capture image"}), 500  # Return error if capture fails


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')

    # Save the code to a temporary .cpp file
    code_file = 'temp_code.cpp'
    with open(code_file, 'w') as f:
        f.write(code)

    try:
        # Compile the C++ code
        compile_process = subprocess.run(['g++', code_file, '-o', 'temp_code'], capture_output=True, text=True)
        if compile_process.returncode != 0:
            return jsonify({"error": compile_process.stderr})

        # Execute the compiled code
        run_process = subprocess.run(['./temp_code'], capture_output=True, text=True)
        if run_process.returncode == 0:
            return jsonify({"output": run_process.stdout})
        else:
            return jsonify({"error": run_process.stderr})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        # Clean up temporary files
        if os.path.exists('temp_code.cpp'):
            os.remove('temp_code.cpp')
        if os.path.exists('temp_code'):
            os.remove('temp_code')

if __name__ == "__main__":
    app.run(debug=True)



