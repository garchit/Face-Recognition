# from deepface import DeepFace
# import os
# # from tensorflow.keras.layers.experimental import LocallyConnected2D

# def match_faces(user_images, folder_path):
#     matched_images = []
#     for user_image in user_images:
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             try:
#                 # Perform face verification using DeepFace
#                 result = DeepFace.verify(user_image, file_path, model_name="VGG-Face")
#                 if result["verified"]:
#                     matched_images.append(file_path)
#                     print(f"Match found: {file_name}")
#             except Exception as e:
#                 print(f"Error processing {file_name}: {e}")
#     return matched_images

import face_recognition

def match_faces_facial_recognition(user_image_paths, folder_image_paths, tolerance=0.6):
    print("inside face_utils file")
    print(user_image_paths)
    print(folder_image_paths)
    user_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(img))[0] for img in user_image_paths]
    matched_files = []

    for file_path in folder_image_paths:
        folder_image = face_recognition.load_image_file(file_path)
        folder_encodings = face_recognition.face_encodings(folder_image)

        for folder_encoding in folder_encodings:
            matches = face_recognition.compare_faces(user_encodings, folder_encoding, tolerance=tolerance)
            if any(matches):
                matched_files.append(file_path)
                print(f"Match found: {file_path}")
                break

    return matched_files
