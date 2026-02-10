# Auto Backup to Google Drive

Automatically zips your project folders and uploads to Google Drive. Keeps only the last 5 versions to save space.

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Place your `client_secrets.json` (from Google Cloud) in this folder
3. Edit `backup.py` and change `self.projects_folder` to your projects directory
4. Run once manually: `python backup.py`
   - It will open a browser to authorize Google Drive (only first time)
5. After first auth, it runs automatically

## Schedule (Run automatically)

### Windows (Task Scheduler)
- Create task to run daily at 6 PM
- Action: `python backup.py`

### Mac/Linux (Cron)
Edit crontab: `crontab -e`
Add line: `0 18 * * * cd /path/to/this/folder && python3 backup.py`

This runs every day at 6:00 PM.

## What gets backed up?
- Each subfolder in your projects folder becomes one zip file
- Excludes: node_modules, .git, __pycache__, venv (to save space)
- Automatically deletes backups older than the last 5 versions