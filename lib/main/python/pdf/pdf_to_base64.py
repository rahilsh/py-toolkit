import base64


def pdf_to_base64(file_path):
    return base64.encodestring(open(file_path, 'rb').read())
