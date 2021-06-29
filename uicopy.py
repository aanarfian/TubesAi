import os
from flask import Flask,jsonify, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import testui
import cv2
import uuid

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = os.path.join('asset', 'upload')
app.config['GBLUR_FOLDER'] = os.path.join('asset', 'gblur')


ALLOWED_EXTENSIONS = set(['png', 'jpg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['POST', 'GET'])
def home():
	energy = 0
	entropy = 0
	intensitas = 0
	kontras = 0
	smoothness = 0
	matang = 0
	mentah = 0
	klasifikasi = 0
	img = None
	gblur = None
	new_filename = ModuleNotFoundError
	if request.method == "POST":
		if request.files:
			image = request.files["file"]
			_, file_ext = os.path.splitext(str(image.filename))
			new_filename = ''.join((str(uuid.uuid1()), file_ext))
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
			gray = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], new_filename), 0)
			gblur = cv2.GaussianBlur(gray, (5, 5), 0)
			cv2.imwrite(os.path.join(app.config['GBLUR_FOLDER'], new_filename), gblur)

			imageData, classified, matangmentah, lookup = testui.process_image(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
			if lookup["matang"]==matangmentah[0]:
				klasifikasi = "Mateng"
				matang = matangmentah[0]
				mentah = matangmentah[1]
			elif lookup["matang"]==matangmentah[1]:
				klasifikasi = "Mateng"
				matang = matangmentah[1]
				mentah = matangmentah[0]
			elif lookup["mentah"]==matangmentah[0]:
				klasifikasi = "Mentah"
				matang = matangmentah[0]
				mentah = matangmentah[1]
			else:
				klasifikasi =  "Mentah"
				matang = matangmentah[1]
				mentah = matangmentah[0]
			print(imageData, classified, matangmentah)
			energy = imageData[0]
			entropy = imageData[1]
			intensitas = imageData[2]
			kontras = imageData[3]
			smoothness = imageData[4]

	# print(energy)
	return render_template("index.html", content=[energy, entropy, intensitas, kontras, smoothness, matang, mentah, klasifikasi, img, gblur, new_filename])

@app.route('/asset/upload/<name>')
def upload_image(name):
	return send_from_directory(app.config['UPLOAD_FOLDER'], name, as_attachment=False)

@app.route('/asset/gblur/<name>')
def gblur_image(name):
	return send_from_directory(app.config['GBLUR_FOLDER'], name, as_attachment=False)

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are png, jpg'})
		resp.status_code = 400
		return resp
	

if __name__ == "__name_-":
    app.run()

