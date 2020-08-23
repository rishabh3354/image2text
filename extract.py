import pytesseract

# adds image processing capabilities
from PIL import Image


def return_string(path):
    # opening an image from the source path
    img = Image.open(path)

    # describes image format in the output
    print(img)
    # path where the tesseract module is installed
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    # converts the image to result and saves it into result variable
    result = pytesseract.image_to_string(img)
    # write text in a text file and save it to source path
    return result



