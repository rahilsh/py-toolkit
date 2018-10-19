import io

import PyPDF2
from wand.image import Image


def convert_pdf_to_img(src_filename, parent_folder, image_name):
    def pdf_page_to_png(src_pdf, pagenum=0, resolution=72, ):
        """
        Returns specified PDF page as wand.image.Image png.
        :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
        :param int pagenum: Page number to take.
        :param int resolution: Resolution for resulting png in DPI.
        """
        dst_pdf = PyPDF2.PdfFileWriter()
        for i in range(src_pdf.getNumPages()):
            dst_pdf.addPage(src_pdf.getPage(i))

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=resolution)
        img.convert("png")

        return img

    # Main
    # ====

    src_pdf = PyPDF2.PdfFileReader(file(src_filename, "rb"))

    # What follows is a lookup table of page numbers within sample_log.pdf and the corresponding filenames.
    pages = [{"pagenum": 0, "filename": parent_folder + image_name}]

    for page in pages:
        big_filename = page["filename"] + ".png"
        # small_filename = page["filename"] + "_small" + ".png"

        img = pdf_page_to_png(src_pdf, pagenum=page["pagenum"], resolution=300)
        img.save(filename=big_filename)

        # # Ensmallen
        # img.transform("", "200")
        # img.save(filename=small_filename)

    # Deal with the cropping for JRS0070.
    jrs0070 = {"pagenum": 0, "filename": image_name}

    img = pdf_page_to_png(src_pdf, pagenum=jrs0070["pagenum"], resolution=300)

    big_filename = jrs0070["filename"] + ".png"
    # small_filename = jrs0070["filename"] + "_small" + ".png"

    # Crop
    img.crop(bottom=1000)

    # Save
    img.save(filename=big_filename)

    # # Ensmallen
    # img.transform("", "200")
    # img.save(filename=small_filename)


convert_pdf_to_img(
    '/Users/rahil.r/Documents/bad.pdf', '/Users/rahil.r/Documents/', "image1")
