import os
import shutil
import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from zipfile import ZipFile

class ProjectBackup:
    def __init__(self):
        # Configuration - CHANGE THESE PATHS
        self.projects_folder = "/path/to/his/projects"  # Example: C:/Users/Name/Documents/Projects
        self.backup_folder_name = "ProjectBackups"
        self.max_backups = 5  # Keep only last 5 backups
        
        # Google Auth
        self.gauth = GoogleAuth()
        self.drive = None
        
    def authenticate(self):
        """Authenticate with Google Drive"""
        try:
            # Load saved client credentials
            self.gauth.LoadCredentialsFile("mycreds.txt")
            
            if self.gauth.credentials is None:
                # Authenticate if they're not there
                self.gauth.LocalWebserverAuth()
            elif self.gauth.access_token_expired:
                # Refresh them if expired
                self.gauth.Refresh()
            else:
                # Initialize the saved creds
                self.gauth.Authorize()
                
            # Save the current credentials to a file
            self.gauth.SaveCredentialsFile("mycreds.txt")
            self.drive = GoogleDrive(self.gauth)
            print("✅ Authenticated with Google Drive")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("Make sure you placed the client_secrets.json file in this folder")
            return False
    
    def zip_project(self, project_path, output_path):
        """Create zip of project folder"""
        project_name = os.path.basename(project_path)
        zip_name = f"{project_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(output_path, zip_name)
        
        print(f"📦 Zipping {project_name}...")
        
        with ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(project_path):
                # Skip node_modules and other heavy folders
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'venv', '.env']]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Created: {zip_name}")
        return zip_path, zip_name
    
    def find_backup_folder(self):
        """Find or create backup folder in Drive"""
        file_list = self.drive.ListFile({'q': f"title='{self.backup_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        
        if file_list:
            return file_list[0]['id']
        else:
            # Create folder
            folder = self.drive.CreateFile({
                'title': self.backup_folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            })
            folder.Upload()
            print(f"📁 Created backup folder: {self.backup_folder_name}")
            return folder['id']
    
    def upload_to_drive(self, file_path, file_name, folder_id):
        """Upload zip to Google Drive"""
        file = self.drive.CreateFile({
            'title': file_name,
            'parents': [{'id': folder_id}]
        })
        file.SetContentFile(file_path)
        file.Upload()
        print(f"☁️ Uploaded: {file_name}")
        return file['id']
    
    def cleanup_old_backups(self, folder_id, project_name):
        """Keep only last N backups per project"""
        query = f"'{folder_id}' in parents and title contains '{project_name}' and trashed=false"
        file_list = self.drive.ListFile({'q': query}).GetList()
        
        # Sort by created date (newest first)
        file_list.sort(key=lambda x: x['createdDate'], reverse=True)
        
        # Delete old backups
        if len(file_list) > self.max_backups:
            for file in file_list[self.max_backups:]:
                print(f"🗑️ Deleting old backup: {file['title']}")
                file.Delete()
    
    def run_backup(self):
        """Main backup process"""
        print(f"🔷 Starting backup session: {datetime.datetime.now()}")
        
        if not self.authenticate():
            return
        
        # Find backup folder
        folder_id = self.find_backup_folder()
        
        # Create temp directory for zips
        temp_dir = "temp_backups"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        try:
            # Scan projects folder
            if not os.path.exists(self.projects_folder):
                print(f"❌ Projects folder not found: {self.projects_folder}")
                return
            
            projects = [f for f in os.listdir(self.projects_folder) if os.path.isdir(os.path.join(self.projects_folder, f))]
            
            if not projects:
                print("No projects found to backup")
                return
            
            print(f"Found {len(projects)} projects to backup")
            
            for project in projects:
                project_path = os.path.join(self.projects_folder, project)
                
                # Create zip
                zip_path, zip_name = self.zip_project(project_path, temp_dir)
                
                # Upload
                self.upload_to_drive(zip_path, zip_name, folder_id)
                
                # Cleanup old backups for this project
                self.cleanup_old_backups(folder_id, project)
                
                # Remove local zip
                os.remove(zip_path)
            
            print(f"✅ Backup complete! All projects saved to Google Drive")
            
        except Exception as e:
            print(f"❌ Error during backup: {e}")
        finally:
            # Cleanup temp folder
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    backup = ProjectBackup()
    backup.run_backup()