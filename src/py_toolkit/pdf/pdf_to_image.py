try:
    from pdf2image import convert_from_path
except ModuleNotFoundError:
    convert_from_path = None


def convert_pdf_to_img(src_filename, parent_folder, prefix):
    if convert_from_path is None:
        raise ImportError("pdf2image is not installed. Install it with: pip install py-toolkit[pdf]")
    pages = convert_from_path(src_filename, 500)
    count = 0
    for page in pages:
        count = count + 1
        page.save(parent_folder + prefix + str(count) + '.jpg', 'JPEG')
