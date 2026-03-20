import imageio.v3 as iio
from pathlib import Path
import os


def get_full_path(relative_path):
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, "..", relative_path)
    return os.path.abspath(full_path)



images = []
for filename in ["0.png", "1.png", "2.png", "1.png"]:
    images.append(iio.imread(filename))
new_name = input("what should the new file be called?")
iio.imwrite(f'{new_name}.gif', images, duration = 160, loop = 0)
