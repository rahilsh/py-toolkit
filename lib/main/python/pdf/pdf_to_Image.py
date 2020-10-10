from pdf2image import convert_from_path


def convert_pdf_to_img(src_filename, parent_folder, prefix):
    pages = convert_from_path(src_filename, 500)
    count = 0
    for page in pages:
        count = count + 1
        page.save(parent_folder + prefix + str(count) + '.jpg', 'JPEG')


convert_pdf_to_img(
    '/Users/rahil.shaikh/code/bitbucket/python/python-test/lib/test/resources/test.pdf',
    '/Users/rahil.shaikh/code/bitbucket/python/python-test/', "image")
