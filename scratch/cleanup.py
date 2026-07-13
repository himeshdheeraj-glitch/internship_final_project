import shutil
import os

def cleanup():
    folders_to_delete = [
        "app/models",
        "app/schemas",
        "app/repositories",
        "app/services",
        "app/routes",
        "app/utils"
    ]
    files_to_delete = [
        "app/dependencies.py",
        "app/config.py",
        "app/database.py"
    ]
    
    for folder in folders_to_delete:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted folder: {folder}")
            
    for f in files_to_delete:
        if os.path.exists(f):
            os.remove(f)
            print(f"Deleted file: {f}")

if __name__ == "__main__":
    cleanup()
