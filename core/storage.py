import json, os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]  # project root containing app.py
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_cv_to_file(data, filename= DATA_DIR / "cv.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    
def delete_cv_file(filename= DATA_DIR / "cv.json"):
    if Path(filename).exists():
        os.remove(filename)

def load_from_file(filename):
    file_path = DATA_DIR / filename
    if Path(file_path).exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
