import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


class GoogleDriveServiceAccount:
    """Google Drive uploader using Service Account authentication"""
    
    def __init__(self, service_account_file='service-account-key.json'):
        """
        Initialize the Google Drive uploader with service account
        
        Args:
            service_account_file (str): Path to the service account JSON key file
        """
        self.service_account_file = service_account_file
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API using Service Account"""
        try:
            if not os.path.exists(self.service_account_file):
                raise FileNotFoundError(f"Service account file not found: {self.service_account_file}")
            
            print(f"Loading service account credentials from: {self.service_account_file}")
            
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file, 
                scopes=self.scopes
            )
            
            # Build the service
            self.service = build('drive', 'v3', credentials=credentials)
            if not self.service:
                raise Exception("Failed to initialize Google Drive API service")
            
            print("Google Drive API service initialized successfully with service account!")
            
        except Exception as e:
            print(f"Authentication error: {e}")
            raise
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Create a folder in Google Drive or return existing one
        
        Args:
            folder_name (str): Name of the folder to create
            parent_folder_id (str): ID of parent folder (optional)
            
        Returns:
            dict: Folder metadata if successful, None otherwise
        """
        try:
            if not self.service:
                print("Google Drive service not initialized")
                return None
                
            # Check if folder already exists
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_folder_id:
                query += f" and parents in '{parent_folder_id}'"
            
            results = self.service.files().list(q=query).execute()
            folders = results.get('files', [])
            
            if folders:
                print(f"Folder '{folder_name}' already exists")
                return folders[0]
            
            # Create new folder
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(body=folder_metadata).execute()
            print(f"Created folder: {folder_name}")
            return folder
            
        except Exception as e:
            print(f"Error creating folder: {e}")
            return None
    
    def upload_file(self, file_path, folder_id=None, file_name=None):
        """
        Upload a file to Google Drive
        
        Args:
            file_path (str): Path to the file to upload
            folder_id (str): ID of the folder to upload to (optional)
            file_name (str): Name for the file on Drive (optional, uses original name if not provided)
            
        Returns:
            dict: File metadata if successful, None otherwise
        """
        try:
            if not self.service:
                print("Google Drive service not initialized")
                return None
                
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None
            
            # Use original filename if no custom name provided
            if not file_name:
                file_name = os.path.basename(file_path)
            
            # Prepare file metadata
            file_metadata = {'name': file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Detect MIME type based on file extension
            file_extension = os.path.splitext(file_path)[1].lower()
            mime_types = {
                '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav',
                '.mp4': 'video/mp4',
                '.avi': 'video/x-msvideo',
                '.txt': 'text/plain',
                '.pdf': 'application/pdf',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png'
            }
            mime_type = mime_types.get(file_extension, 'application/octet-stream')
            
            # Create media upload
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            # Upload the file
            print(f"Uploading file: {file_name}")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,size'
            ).execute()
            
            print(f"Successfully uploaded: {file_name}")
            return file
            
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
    
    def list_files(self, folder_id=None, max_results=10):
        """
        List files in Google Drive
        
        Args:
            folder_id (str): ID of folder to list files from (optional)
            max_results (int): Maximum number of files to return
            
        Returns:
            list: List of file metadata
        """
        try:
            if not self.service:
                print("Google Drive service not initialized")
                return []
                
            query = "trashed=false"
            if folder_id:
                query += f" and parents in '{folder_id}'"
            
            results = self.service.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id,name,size,modifiedTime,webViewLink)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def delete_file(self, file_id):
        """
        Delete a file from Google Drive
        
        Args:
            file_id (str): ID of the file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.service:
                print("Google Drive service not initialized")
                return False
                
            self.service.files().delete(fileId=file_id).execute()
            print(f"File deleted: {file_id}")
            return True
            
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
