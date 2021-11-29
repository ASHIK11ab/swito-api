from flask import (Flask, send_from_directory, request, 
                    make_response, jsonify)
from utils import app_key_required
import os

app = Flask(__name__)
app.config.from_object('configuration.Config')

@app.route('/')
def index():
  return """
    <h1>API used by Swito to store and manage files.</h1>
    <h3>Created by Ashik Meeran Mohideen S</h3>
    """


@app.route('/images/upload', methods=["POST"])
@app_key_required
def upload_file():
  category = request.args.get('category')
  file_id = request.args.get('id')
  UPLOADS_FOLDER = f"{app.config['IMAGES_FOLDER']}/{category}"

  # Return error response if no file in POST request.
  if 'file' not in request.files:
    response = { "message": "File part missing" }
    return make_response(jsonify(response), 404)

  file = request.files.get('file')

  filename = f"{file_id}.jpeg"
  file.save(os.path.join(UPLOADS_FOLDER, filename))

  response = {
    "message": "File upload successfull",
    "file_url": f"{app.config['APP_DOMAIN']}/{UPLOADS_FOLDER}/view/{filename}"
  }

  return make_response(jsonify(response), 200)


@app.route('/images/view/<path:filename>')
def send_image(filename):
  category = request.args.get('category')
  UPLOADS_FOLDER = f"{app.config['IMAGES_FOLDER']}/{category}"

  try:
    return send_from_directory(UPLOADS_FOLDER, filename)
  except:
    response = { "message": "File not found !" }
    return make_response(jsonify(response), 404)


if __name__ == "__main__":
  with app.app_context():
    app.run()