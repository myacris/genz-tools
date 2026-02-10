# File Organizer

Automatically organizes your Downloads folder (or any folder) by file type.

## Usage

1. Run: python organizer.py
2. Files will be sorted into folders: Images, Documents, Videos, Audio, Archives, Code, Executables, Fonts, Others
3. Check organization_log.txt to see what was moved

## Schedule Automatic Organization (Windows)
- Open Task Scheduler
- Create Basic Task
- Trigger: Daily or Weekly
- Action: Start a program
- Program: python
- Arguments: organizer.py

## Schedule (Mac/Linux)
Add to crontab:
0 9 * * * /usr/bin/python3 /path/to/organizer.py
(This runs every day at 9 AM)