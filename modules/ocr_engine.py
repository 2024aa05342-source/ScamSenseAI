import easyocr
reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):

    result = reader.readtext(image_path)

    extracted_text = ""

    for item in result:
        extracted_text += item[1] + "\n"

    return extracted_text