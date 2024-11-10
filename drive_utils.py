from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import os


from googleapiclient.errors import HttpError
# Define the scopes for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """
    Authenticates with Google Drive using a service account.
    """
    creds = service_account.Credentials.from_service_account_file(
        'project-img-441110-419d7deec7b5.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id):
    """
    Lists all files in a specified Google Drive folder.

    Args:
        service: The authenticated Google Drive service instance.
        folder_id: ID of the Google Drive folder to list files from.

    Returns:
        A list of files in the specified folder.
    """
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items

def download_file(service, file_id, file_name):
    """
    Downloads a file from Google Drive.

    Args:
        service: The authenticated Google Drive service instance.
        file_id: ID of the file to download.
        file_name: Name to save the downloaded file as.

    Returns:
        The path to the downloaded file.
    """
    file_path = os.path.join('', file_name)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")

    fh.close()
    return file_path

def create_folder(service, folder_name):
    """
    Creates a new folder in Google Drive.

    Args:
        service: The authenticated Google Drive service instance.
        folder_name: The name of the new folder.

    Returns:
        The ID of the newly created folder.
    """
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def upload_file(service, file_path, folder_id):
    """
    Uploads a file to a specified folder in Google Drive.

    Args:
        service: The authenticated Google Drive service instance.
        file_path: Path to the file to upload.
        folder_id: ID of the Google Drive folder to upload to.

    Returns:
        The ID of the uploaded file.
    """
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# def set_folder_permissions(service, folder_id, email):
#     # Define the permission for the folder (Editor access)
#     permission = {
#         'type': 'user',
#         'role': 'reader',  # Or 'writer' for editing permissions
#         'emailAddress': email
#     }

#     # Grant access to the folder
#     service.permissions().create(
#         fileId=folder_id,
#         body=permission,
#         fields='id'
#     ).execute()

#     print(f"Permission granted to {email} for folder {folder_id}")


def share_folder(service, folder_id, role='reader', type='anyone', email=None):
    """Share the folder with anyone or specific email"""
    permission = {
        'type': type,  # 'user' for specific user, 'anyone' for public access
        'role': role,  # 'reader' for read-only, 'writer' for write access
    }
    
    if type == 'user' and email:
        permission['emailAddress'] = email  # If sharing with specific user, add email

    try:
        # Add the permission to the folder
        service.permissions().create(
            fileId=folder_id,
            body=permission,
            fields='id'
        ).execute()
        print(f"Folder {folder_id} shared successfully with {type} ({role}).")
    except HttpError as error:
        print(f"An error occurred while sharing the folder: {error}")



# if __name__ == "__main__":
#     service = authenticate_google_drive()
#     # List the first 10 files in your Google Drive
#     results = service.files().list(pageSize=10, fields="files(id, name)").execute()
#     items = results.get('files', [])

#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(f"{item['name']} ({item['id']})")
            
# if __name__ == "__main__":
#     service = authenticate_google_drive()
#     folder_id = 'your-folder-id'  # Replace with the folder ID containing images
    
#     # List files in the Google Drive folder
#     files = list_files_in_folder(service, folder_id)
    
#     # Download each file in the folder
#     for file in files:
#         print(f"Downloading {file['name']}...")
#         file_path = download_file(service, file['id'], file['name'])
#         print(f"Downloaded to {file_path}")
          
            
            

# if __name__ == "__main__":
#     service = authenticate_google_drive()
#     # List the first 10 files in your Google Drive
#     results = service.files().list(pageSize=10, fields="files(id, name)").execute()
#     items = results.get('files', [])

#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(f"{item['name']} ({item['id']})")


# if __name__ == "__main__":
#     print("Authenticating Google Drive...")
#     service = authenticate_google_drive()
#     print("Authenticated successfully.")

#     # Replace this with your actual folder URL for testing
#     drive_folder_url = "YOUR_GOOGLE_DRIVE_FOLDER_URL"  
#     folder_id = extract_folder_id(drive_folder_url)
#     print(f"Extracted Folder ID: {folder_id}")

#     if folder_id:
#         print("Listing files in folder...")
#         files = list_files_in_folder(service, folder_id)
#         if not files:
#             print("No files found in the specified folder.")
#         else:
#             for file in files:
#                 print(f"File found: {file['name']} ({file['id']})")
#                 print(f"Downloading {file['name']}...")
#                 download_file(service, file['id'], file['name'])
#     else:
#         print("Failed to extract folder ID.")
