from pathlib import Path
import os
import random
import shutil

test_image_number = 40

parts = ["32316", "32140", "32270", "2780", "32073"]

dirname = os.path.dirname(__file__)

path_to_test_folder = os.path.join(dirname, "pictures/test/")
path_to_train_folder = os.path.join(dirname, "pictures/train/")
Path(path_to_test_folder).mkdir(parents=True, exist_ok=True)
Path(path_to_train_folder).mkdir(parents=True, exist_ok=True)

path_to_pictures = os.path.join(dirname, "pictures/edited/")


def main():
    shutil.rmtree(path_to_test_folder)
    shutil.rmtree(path_to_train_folder)


    for part_number in parts:
        src_path = path_to_pictures + part_number
        train_dst_path = path_to_train_folder + part_number
        test_dst_path = path_to_test_folder + part_number

        files = os.listdir(src_path)
        for i in range(test_image_number):
            Path(test_dst_path).mkdir(parents=True, exist_ok=True)

            file = random.choice(files)
            files.remove(file)
            shutil.copy(src_path + f"/{file}", test_dst_path + f"/{file}")

        for file in files:
            Path(train_dst_path).mkdir(parents=True, exist_ok=True)
            shutil.copy(src_path + f"/{file}", train_dst_path + f"/{file}")


if __name__ == "__main__":
    main()
