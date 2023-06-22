from PIL import Image
import pillow_heif
import os

path = "C:\\Users\\%username%\\Downloads\\heic"

i = 1

for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
        heif_file = pillow_heif.read_heif(path + "\\" + file)

        print(str(i) + ") " + file + ".........", end = "")

        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )

        image.save("C:\\Users\\%username%\\Downloads\\jpg\\" + file[:-5] + ".png" , format="png")
        
        i += 1
        
        print("Success")