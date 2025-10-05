import os

BASE_FOLDER = os.environ.get("LCKT_BASE_FOLDER", r"C:\LocalCloudKT")

os.makedirs(BASE_FOLDER, exist_ok=True)

def safe_join(base, *paths):
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(os.path.abspath(base)):
        raise ValueError("Недопустимый путь")
    return final_path
