import csv
import io
import json
import logging
import os
import shutil
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


def delete_dir(path):
    shutil.rmtree(path, ignore_errors=True)


def main():
    with open('/Users/rahil.r/Documents/temp/practo/july_sept/fuel_1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                print "Processing userID: {}".format(row['userid'])
                url = 'https://api.gw.zetapay.in/zeta.in/biller/1.0/userBills?token=U3N5VTlXMndFZGFyK1hhbzR5Y1BraEl3RTl2RExzRU14MU0vSkxSb1Vjc3M5ZXJpOkFRRUM2UXNyWTBtanlRZFZ4WEp0LzlpMjJSbXRFWVNUVmdqUTA0WjlHUG1rNWw1RTBQTmdla3FSM0NjV2h6ZEVaaW15QldDdURXOEtiUndmcDNRVys0c0tQQmhoSDNETmpIRzI3S01acDhlNkhvYnJHcytGOXJycHdSMGc1cjVZTUI2TUdWMHAvRHFnWEtvMlE0OU43UT09&userID=' + \
                      row['userid'] + '&count=100&cardID=' + row['card_id']
                response, status = request(method='GET',
                                           url=url)
                if status is not 200:
                    print "Response not 200. response: {}, Status: {}, userID: {}".format(response, status,
                                                                                          str(row['userid']))
                else:
                    path = '/Users/rahil.r/Documents/temp/practo/july_sept/fuel/' + str(row['userid']) + '/'
                    delete_dir(path)
                    make_dir_from_path(path)
                    print "Creating user folder and saving json"
                    with io.open(path + row['userid'] + '.json', 'w', encoding='utf8') as outfile:
                        outfile.write(to_unicode(response))
                    if len(json.loads(response)["bills"]) == 0:
                        # print "No bill for user: {}".format(str(row['userid']))
                        continue
                    for bill in json.loads(response)["bills"]:
                        unique_bill_key = ''
                        if 'billNumber' in bill['attrs']:
                            unique_bill_key = bill['attrs']['billNumber']
                        if unique_bill_key == '':
                            # print "Bill No not present, hence using claimID"
                            unique_bill_key = bill['claimId']
                        unique_bill_key = unique_bill_key.replace('/', '_')
                        # if unique_bill_key in {'a1478', ' ZFMCGWRL-03-2018-0000796', 'RBLBXYRH-03-2018-0001940',
                        #                        'XTCIGVIL-03-2018-0001905', 'GJAKPAQG-03-2018-0001281',
                        #                        'SJPHPXGY-03-2018-0000830', ': FZABMYBC-03-2018-0001069',
                        #                        ': KIAGGOMO-03-2018-0001063', 'VJBQHTVZ-03-2018-0000933',
                        #                        ':AXFLVWNQ-03-2018-0001073', 'HNVPWVBQ-03-2018-0000460',
                        #                        'XFNYJHJE-03-2018-0001820', 'WBOEZCWL-03-2018-0025893',
                        #                        'IKJTHMWI-03-2018-0000949', ' GNKJXDWC-03-2018-0002000',
                        #                        ': MXAHFZLR-03-2018-0004419', 'ZOOYJBST-03-2018-0000947',
                        #                        'GHOMJMLE-03-2018-0001649', 'IWKZLCOE-03-2018-0001419',
                        #                        'LMTJDLSD-03-2018-0000270', 'IDMYPYGI-03-2018-0000614',
                        #                        'DFGNCLGJ-03-2018-0001265', 'QWIJEYSS-03-2018-0000320',
                        #                        'ODLIGYVO-03-2018-0000013', 'VECZJGAI-03-2018-0001517',
                        #                        'IQEVCKVQ-03-2018-0000639', 'ADPVTPWU-03-2018-0000117',
                        #                        'VRUFKOML-03-2018-0001943', ': AJCMGZOX-03-2018-0000387',
                        #                        'ZKHLNTXZ-03-2018-0001383', 'TQNBMLZZ-03-2018-0001196',
                        #                        'GPADKHWG-03-2018-0001354', 'XGZQNPDT-03-2018-0000625',
                        #                        ' HQRIEDRE-03-2018-0001595', 'VVITVQBC-03-2018-0001796',
                        #                        'PFZDAYAS-03-2018-0003144', 'JGSYCWJY-03-2018-0008524',
                        #                        'AYHJIXCT-03-2018-0001153', 'SLSRQNEF-03-2018-0000239', '13961',
                        #                        'UEAQEFLW-03-2018-0082147', 'CJXYFQCP-03-2018-0000003', '5906634013',
                        #                        'TUBIUYQT-03-2018-0003313', 'SYHXFEEV-03-2018-0000557',
                        #                        'SALVFUNP-03-2018-0001012', 'YNTTMFZH-03-2018-0000917',
                        #                        ' HMCQKCUZ-03-2018-0000952', 'UEAQEFLW-03-2018-0095569',
                        #                        ': IWKZLCOE-03-2018-0001419', 'IEKHLNVY-03-2018-0000925',
                        #                        'RYMDRBCI-03-2018-0000913', ': WCQZFMEL-03-2018-0001706',
                        #                        'QSMVPELY-03-2018-0001001', 'JECKATCT-03-2018-0001354',
                        #                        'EMZVBJTW-03-2018-0001089', 'NHXWNZBR-03-2018-0003230',
                        #                        'GUBQIKJW-03-2018-0000232', 'IISQSWTY-03-2018-0001053',
                        #                        ': PNHMJTKO-03-2018-0000752', ': CQLRBUGS-03-2018-0001589',
                        #                        'JXUZNSAX-03-2018-0000654', 'TWWYRZFT-03-2018-0000801', '200051207',
                        #                        'ZQENPZFH-03-2018-0002549', ': PYSHYNNJ-03-2018-0002691',
                        #                        ': MPEUNBKL-03-2018-0001241'}:
                        #     print("skipping as it is already processed")
                        #     continue
                        # if unique_bill_key in {'10ika06816687555',
                        #                        '34183b45-be16-4177-a144-b5559f71cf34_1537195222158-VAVC',
                        #                        '34183b45-be16-4177-a144-b5559f71cf34_1537195953800-LVFo'}:
                        #     print("skipping as pdf is pass protected")
                        #     continue
                        print "Processing bill no: {}".format(unique_bill_key.encode('utf-8'))
                        if bill['uploadedAt'] is not None and (
                                bill['uploadedAt'] < 1530297000000 or bill['uploadedAt'] > 1538332200000):
                            print("skipping as bill is of previous financial year")
                            continue
                            # if bill['state'] == 'PAID' or bill['state'] == 'PARTIALLY_PAID' or bill[
                            #     'state'] == 'APPROVED' or bill['state'] == 'UNPAID':
                        # print "Bill is Approved"
                        bills_folder_path = path + 'bills/' + unique_bill_key
                        make_dir_from_path(bills_folder_path)
                        count = 1
                        for billUrl in bill["billUrls"]:
                            actual_bill = urllib2.urlopen(billUrl)
                            extn = '.jpg'
                            if actual_bill.headers['content-type'] == 'application/pdf':
                                extn = '.pdf'
                            elif actual_bill.headers['content-type'] == 'image/png':
                                extn = '.png'
                            elif actual_bill.headers['content-type'] != 'image/jpeg':
                                print "Bill not of jpg and pdf type. User {}, billNo: {}, content-type: {}".format(
                                    str(row['userid']),
                                    unique_bill_key.encode(
                                        'utf-8'), str(actual_bill.headers['content-type']))
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
                        # else:
                        #     print "Skipping bill as it is not approved. BillNo: {}".format(
                        #         unique_bill_key.encode('utf-8'))
            except Exception as e:
                print "Error while processing user: {}".format(str(row['userid']))
                logging.exception(
                    "Error while processing User: " + str(row['userid']))

    print "Done !!!"


if __name__ == '__main__':
    main()
