import os

def fix_imports():
    targets = [
        "app/users/repositories.py",
        "app/properties/repositories.py",
        "app/amenities/repositories.py",
        "app/favorites/repositories.py",
        "app/reviews/repositories.py"
    ]
    
    for path in targets:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace target import
            updated = content.replace(
                "from app.repositories.base_repository import BaseRepository",
                "from app.shared.base_repository import BaseRepository"
            )
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"Fixed imports in: {path}")

if __name__ == "__main__":
    fix_imports()
