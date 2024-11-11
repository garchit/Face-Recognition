from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import os


from googleapiclient.errors import HttpError
# Define the scopes for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    
    # Authenticates with Google Drive using a service account.
    
    creds = service_account.Credentials.from_service_account_file(
        'project-img-441110-14d3080721e5.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id):
    
    # Lists all files in a specified Google Drive folder.

    
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items

def download_file(service, file_id, file_name):
    
# Downloads a file from Google Drive.

# The path to the downloaded file.
    
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
    
#  Creates a new folder in Google Drive.

# Returns:
 # The ID of the newly created folder.
    
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(folder)
    return folder.get('id')

def upload_file(service, file_path, folder_id):
    
# Uploads a file to a specified folder in Google Drive.
# The ID of the uploaded file.
    
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')



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

