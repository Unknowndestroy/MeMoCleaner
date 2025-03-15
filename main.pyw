import os
import shutil
import sys
import time
from win10toast import ToastNotifier

# Windows Startup folder
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\Windows\Start Menu\Programs\Startup')
script_path = os.path.abspath(sys.argv[0])
destination_path = os.path.join(startup_folder, 'startup_cleaner.py')

# Copy itself to startup folder
if script_path != destination_path:
    shutil.copy(script_path, destination_path)

# Show notification
notifier = ToastNotifier()
notifier.show_toast("MeMo Cleaner", "Cleaning process started...", duration=5)

def clean():
    temp_folders = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        os.path.join(os.getenv('WINDIR'), 'Temp'),
        os.path.join(os.getenv('WINDIR'), 'Prefetch'),
        os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Temp'),
        os.path.join(os.getenv('USERPROFILE'), 'Recent'),
        os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Recent'),
        os.path.join(os.getenv('WINDIR'), 'SoftwareDistribution', 'Download'),
        os.path.join(os.getenv('WINDIR'), 'System32', 'LogFiles'),
        os.path.join(os.getenv('WINDIR'), 'System32', 'wbem', 'Logs'),
        os.path.join(os.getenv('WINDIR'), 'SysWOW64', 'wbem', 'Logs')
    ]

    download_folders = [
        os.path.join(os.getenv('USERPROFILE'), 'Downloads'),
        'D:\\Downloads'
    ]
    
    for folder in temp_folders:
        if folder and os.path.exists(folder):
            try:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                        except Exception:
                            pass
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        try:
                            shutil.rmtree(dir_path)
                        except Exception:
                            pass
            except Exception:
                pass
    
    # Clean Downloads folder with specific filters
    delete_extensions = {'.log', '.crdownload', '.tmp'}
    for folder in download_folders:
        if os.path.exists(folder):
            try:
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if os.path.isfile(file_path) and file.endswith(tuple(delete_extensions)):
                        try:
                            os.remove(file_path)
                        except Exception:
                            pass
            except Exception:
                pass

    notifier.show_toast("MeMo Cleaner", "Unnecessary files have been cleaned!", duration=5)

# Start cleaning
clean()
