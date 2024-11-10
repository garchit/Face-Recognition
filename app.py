from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from drive_utils import authenticate_google_drive, download_file, list_files_in_folder, create_folder, upload_file  , share_folder
from face_utils import match_faces_facial_recognition  # Ensure face_utils.py has the match_faces function implemented

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'user_images'
app.config['TEMP_FOLDER'] = 'temp'  # Directory for downloaded images

# Ensure the folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    folder_link = request.form['folderLink']
    images = request.files.getlist('images')
    print(folder_link)
    print(images)

    # Step 1: Save the uploaded images to the server
    user_image_paths = []
    print("here")
    for image in images:
        filename = secure_filename(image.filename)
        print(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(file_path)
        user_image_paths.append(file_path)

    # Step 2: Extract folder ID from the Google Drive folder link
    folder_id = folder_link.split('/')[-1]

    # Step 3: Authenticate and list files in the Google Drive folder
    service = authenticate_google_drive()
    files = list_files_in_folder(service, folder_id)
    print(files)
    # Step 4: Download files from Google Drive into the 'temp' folder
    downloaded_files = []
    for file in files:
        print(f"Downloading {file['name']}...")
        file_path = download_file(service, file['id'], os.path.join(app.config['TEMP_FOLDER'], file['name']))
        print(f"Downloaded to {file_path}")
        downloaded_files.append(file_path)

    # Step 5: Perform face matching between user images and downloaded images
    matched_files = match_faces_facial_recognition(user_image_paths, downloaded_files)

    # Step 6: Create a new folder in Google Drive for matched images
    matched_folder_id = create_folder(service, 'Matched Images Folder')

    # Step 7: Upload matched images to the new Google Drive folder
    for file_path in matched_files:
        upload_file(service, file_path, matched_folder_id)
        print(f"Uploaded matched file: {file_path}")

    share_folder(service, matched_folder_id, role='reader', type='anyone', email='someone@example.com')

    # user_email = 'gargarchit355@gmail.com'  # Replace with the email you want to give access
    # set_folder_permissions(service, matched_folder_id, user_email)
    
    # Optional Step 8: Clean up 'temp' directory after uploading
    for file_path in downloaded_files:
        os.remove(file_path)
    for file_path in user_image_paths:
        os.remove(file_path)

    return jsonify({"message": "Matched files uploaded successfully", "matched_folder_id": matched_folder_id})

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, request, render_template, redirect, url_for
# from werkzeug.utils import secure_filename
# import os
# from drive_utils import authenticate_google_drive, list_files_in_folder, download_file, create_folder, upload_file
# from face_utils import match_faces

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         drive_folder_link = request.form["drive_folder_link"]

#         user_images = []
#         if "user_images" in request.files:
#             uploaded_files = request.files.getlist("user_images")
#             for file in uploaded_files:
#                 filename = secure_filename(file.filename)
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(file_path)
#                 user_images.append(file_path)

#         service = authenticate_google_drive()
#         folder_id = drive_folder_link.split('/')[-1]
#         drive_files = list_files_in_folder(service, folder_id)
#         downloaded_files = [download_file(service, f['id'], f['name']) for f in drive_files]

#         matched_files = match_faces(user_images, 'temp')

#         matched_folder_id = create_folder(service, 'Matched Images Folder')
#         for file_path in matched_files:
#             upload_file(service, file_path, matched_folder_id)

#         return "Face matching complete and matched images uploaded to Google Drive."

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)
