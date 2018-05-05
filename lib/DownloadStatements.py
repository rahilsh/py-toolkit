import csv
import io
import json
import logging
import os
import urllib2

import PyPDF2
import requests
from wand.image import Image

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def request(method, url, headers=None, params=None, data=None):
    response = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)
        response_text = response.text
        response_status = response.status_code
        return response_text, response_status
    except Exception as e:
        print "Error while making API call to Method: {}, URL: {}, headers: {}, params: {}, data: {}".format(
            method, url, headers, params, data)
        print "Error: {}".format(str(e))
        exit(1)
    finally:
        if response is not None:
            response.close()


def make_dir_from_path(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


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


def main():
    with open('/Users/rahil.r/Documents/test_2.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                print "Processing userID: {}".format(row['userid'])
                url = 'https://api.gw.zetapay.in/zeta.in/biller/1.0/userBills?token=QnQvMWJhVk9qUG5YK3NvbVlXd3kwQ2FxN2RaMzZsUy9IYlVFSFNjL09GSmZqNEFOOkFRRWRCbzc5MlU1eHkxZ05aY21ac0l1ZTVpZVk5ZW1pZ1VaRCtLL1cweE81TC9KMjJxTmNYRXhVTUNCSTBvY0k0RURSdHIvOUlYVU1GNElneFE2OWk1TUdYcGo5NWVlamtsTDNhVXVzUHhLSE9HT2hCSW55eksyZ1BDT1Y5U3BBUzhORkR2dWlQNDQxam56Q3pyWExJL1orcWdnPQ==&userID=' + \
                      row['userid'] + '&cardProgramID=23c65c87-444a-4eb7-af70-bfb36ff91f3b&count=100'
                response, status = request(method='GET',
                                           url=url)
                if status is not 200:
                    print "response: {}, Status: {}, userID: {}".format(response, status, str(row['userid']))
                else:
                    path = '/Users/rahil.r/Documents/practo/' + str(row['userid']) + '/'
                    make_dir_from_path(path)
                    print "Creating user folder and saving json"
                    with io.open(path + row['userid'] + '.json', 'w', encoding='utf8') as outfile:
                        outfile.write(to_unicode(response))
                    if len(json.loads(response)["bills"]) == 0:
                        print "No bill for user: {}".format(str(row['userid']))
                        continue
                    for bill in json.loads(response)["bills"]:

                        unique_bill_key = bill['attrs']['billNumber']
                        if unique_bill_key == '':
                            print "Bill No not present, hence using claimID"
                            unique_bill_key = bill['claimId']
                        unique_bill_key = unique_bill_key.replace('/', '_')
                        print "Processing bill no: {}".format(unique_bill_key.encode('utf-8'))
                        if bill['state'] == 'PAID' or bill['state'] == 'PARTIALLY_PAID' or bill[
                            'state'] == 'APPROVED' or bill['state'] == 'UNPAID':
                            print "Bill is Approved"
                            bills_folder_path = path + 'bills/' + unique_bill_key
                            make_dir_from_path(bills_folder_path)
                            count = 1
                            for billUrl in bill["billUrls"]:
                                actual_bill = urllib2.urlopen(billUrl)
                                extn = '.jpg'
                                if actual_bill.headers['content-type'] == 'application/pdf':
                                    extn = '.pdf'
                                elif actual_bill.headers['content-type'] != 'image/jpeg':
                                    print "Bill not of jpg and pdf type. User {}, billNo".format(str(row['userid']),
                                                                                                 str(unique_bill_key))
                                with open(
                                        bills_folder_path + '/' + unique_bill_key + '_' + str(
                                            count) + extn,
                                        'wb') as output:
                                    output.write(actual_bill.read())

                                if extn == '.pdf':
                                    convert_pdf_to_img(
                                        bills_folder_path + '/' + unique_bill_key + '_' + str(
                                            count) + extn, bills_folder_path + '/',
                                        unique_bill_key + '_' + str(
                                            count))
                                count = count + 1
                        else:
                            print "Skipping bill as it is not approved. BillNo: {}".format(
                                str(unique_bill_key))
            except Exception as e:
                print "Error while processing user: {}".format(str(row['userid']))
                logging.exception(
                    "Error while processing User: " + str(row['userid']))

    print "Done !!!"


if __name__ == '__main__':
    main()
