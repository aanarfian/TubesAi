import os
from flask import Flask,jsonify, render_template, request, redirect
from werkzeug.utils import secure_filename
import testui
import cv2

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = os.path.join('asset', 'upload')


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
	if request.method == "POST":
		if request.files:
			image = request.files["file"]
			# print(image)
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
			img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image.filename, 1))
			gray = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image.filename, 0))
			gblur = cv2.GaussianBlur(gray, (5, 5), 0)

			imageData, classified, matangmentah, lookup = testui.process_image(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
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
	return render_template("index.html", content=[energy, entropy, intensitas, kontras, smoothness, matang, mentah, klasifikasi, img, gblur])

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

