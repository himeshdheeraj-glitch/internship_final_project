import os

def create_modular_dirs():
    features = [
        "auth", "users", "properties", "reviews", "favorites",
        "amenities", "locations", "notifications", "analytics",
        "core", "database", "shared"
    ]
    
    for f in features:
        path = f"app/{f}"
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as out:
                pass
                
    print("Modular directory structure created.")

if __name__ == "__main__":
    create_modular_dirs()
