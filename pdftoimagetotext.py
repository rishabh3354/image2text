from pdf2image import convert_from_path


def pdf_to_image(pdf_path):

    pages = convert_from_path(pdf_path, 500)

    # Counter to store images of each page of PDF to image
    image_counter = 1
    image_path_all = list()
    # Iterate through all the pages stored above
    for page in pages:
        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        temp_file_name = pdf_path.split(".")[0]

        filename = f"{temp_file_name}_page_" + str(image_counter) + ".jpg"

        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1

        image_path_all.append(filename)

    return image_path_all

