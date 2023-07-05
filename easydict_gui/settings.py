from pathlib import Path

# path to the pictures
images = dict()
for img_path in (Path(__file__).parent / "images").iterdir():
    images[img_path.name] = img_path
