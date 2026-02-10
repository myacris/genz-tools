import os
import shutil
from datetime import datetime
from pathlib import Path

class DownloadsOrganizer:
    def __init__(self, target_folder=None):
        # If no folder specified, use default Downloads
        if target_folder is None:
            self.target_folder = str(Path.home() / "Downloads")
        else:
            self.target_folder = target_folder
        
        # Define categories and extensions
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'Code': ['.py', '.js', '.html', '.css', '.json', '.xml', '.sql', '.php', '.rb', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs'],
            'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.AppImage'],
            'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot']
        }
        
        self.log_file = "organization_log.txt"
    
    def organize(self):
        """Main organization logic"""
        if not os.path.exists(self.target_folder):
            print(f"Error: Folder {self.target_folder} not found")
            return
        
        moved_count = 0
        log_entries = []
        
        # Create category folders
        for category in self.categories.keys():
            folder_path = os.path.join(self.target_folder, category)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {category}")
        
        # Create 'Others' folder for uncategorized files
        others_path = os.path.join(self.target_folder, 'Others')
        if not os.path.exists(others_path):
            os.makedirs(others_path)
        
        # Scan files
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            
            # Skip if it's a directory
            if os.path.isdir(file_path):
                continue
            
            # Skip the script itself and log files
            if filename.endswith('.py') or filename == self.log_file:
                continue
            
            # Get file extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # Find category
            category = 'Others'
            for cat_name, extensions in self.categories.items():
                if ext in extensions:
                    category = cat_name
                    break
            
            # Move file
            dest_folder = os.path.join(self.target_folder, category)
            dest_path = os.path.join(dest_folder, filename)
            
            # Handle duplicates (add number if file exists)
            counter = 1
            original_dest = dest_path
            while os.path.exists(dest_path):
                name, extension = os.path.splitext(filename)
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{extension}")
                counter += 1
            
            try:
                shutil.move(file_path, dest_path)
                moved_count += 1
                log_entry = f"[{datetime.now()}] Moved: {filename} -> {category}/"
                log_entries.append(log_entry)
                print(log_entry)
            except Exception as e:
                error_msg = f"[{datetime.now()}] Error moving {filename}: {e}"
                log_entries.append(error_msg)
                print(error_msg)
        
        # Write log
        with open(os.path.join(self.target_folder, self.log_file), 'a', encoding='utf-8') as f:
            f.write(f"\n--- Organization Session: {datetime.now()} ---\n")
            for entry in log_entries:
                f.write(entry + "\n")
            f.write(f"Total files moved: {moved_count}\n")
        
        print(f"\n✅ Organization complete! Moved {moved_count} files.")
        print(f"📄 Log saved to {self.log_file}")

if __name__ == "__main__":
    # You can change the path below to organize any folder
    # Leave empty to use default Downloads folder
    
    organizer = DownloadsOrganizer()  # Uses default Downloads
    # organizer = DownloadsOrganizer("/path/to/custom/folder")  # Custom path
    
    print("Starting file organization...")
    organizer.organize()