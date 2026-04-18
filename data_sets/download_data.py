import os
import requests
import zipfile
import shutil

# 📁 Target folder
DATA_DIR = "data"
ZIP_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
ZIP_PATH = os.path.join(DATA_DIR, "dataset.zip")

# ✅ Create data folder
os.makedirs(DATA_DIR, exist_ok=True)

# 🚀 Download ZIP
if not os.path.exists(ZIP_PATH):
    print("📥 Downloading dataset...")
    r = requests.get(ZIP_URL)
    with open(ZIP_PATH, "wb") as f:
        f.write(r.content)
    print("✅ Download complete!")
else:
    print("⚡ Dataset already downloaded")

# 📦 Extract ZIP
print("📦 Extracting...")
with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_DIR)

# 📁 Move required files
src_folder = os.path.join(DATA_DIR, "ml-latest-small")

files_needed = ["movies.csv", "links.csv"]

for file in files_needed:
    src = os.path.join(src_folder, file)
    dst = os.path.join(DATA_DIR, file)

    if os.path.exists(src):
        shutil.move(src, dst)

# 🧹 Clean unnecessary files
shutil.rmtree(src_folder, ignore_errors=True)
os.remove(ZIP_PATH)

print("🎉 Data setup complete! Files ready in /data folder")