import os
import requests
import zipfile

DATA_DIR = "data_sets"
ZIP_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
ZIP_PATH = os.path.join(DATA_DIR, "dataset.zip")

os.makedirs(DATA_DIR, exist_ok=True)

# Download ZIP
if not os.path.exists(ZIP_PATH):
    print("Downloading dataset...")
    r = requests.get(ZIP_URL)
    with open(ZIP_PATH, "wb") as f:
        f.write(r.content)
    print("Download complete!")

# Extract ZIP
with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_DIR)

print("Extracted successfully!")

# Move needed files to main data folder
src_folder = os.path.join(DATA_DIR, "ml-latest-small")

for file in ["movies.csv", "links.csv"]:
    src = os.path.join(src_folder, file)
    dst = os.path.join(DATA_DIR, file)

    if os.path.exists(src):
        os.replace(src, dst)

print("✅ Data ready!")