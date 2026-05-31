import csv
import io
import json
import logging
from urllib.request import urlopen

from py_toolkit.utils.folder_util import delete_dir
from py_toolkit.utils.folder_util import make_dir_from_path
from py_toolkit.pdf.pdf_to_image import convert_pdf_to_img
from py_toolkit.utils.request_util import request
from py_toolkit.utils.unicode_util import to_unicode

quarter_folder = '/Users/rahil.r/Documents/tmp/folder/oct_dec/'
program_type = 'asset'
list_of_user_cards = quarter_folder + program_type + '.csv'
program_folder_path = quarter_folder + program_type + '/'
uploaded_at_start_date = '20180930'
uploaded_at_end_date = '20190101'

token = ''

api_url = 'https://localhost/userBills?token=' + token


def process_bill(user_id, path, bill):
    unique_bill_key = ''
    if 'billNumber' in bill['attrs']:
        unique_bill_key = bill['attrs']['billNumber']
    if unique_bill_key == '':
        unique_bill_key = bill['claimId']
    unique_bill_key = unique_bill_key.replace('/', '_')
    print("Processing bill no: {}".format(unique_bill_key.encode('utf-8')))
    bills_folder_path = path + 'bills/' + unique_bill_key
    make_dir_from_path(bills_folder_path)
    process_bill_urls(bill, bills_folder_path, unique_bill_key, user_id)


def process_bill_urls(bill, bills_folder_path, unique_bill_key, user_id):
    count = 1
    for billUrl in bill["billUrls"]:
        actual_bill = urlopen(billUrl)
        extn = '.jpg'
        if actual_bill.headers['content-type'] == 'application/pdf':
            extn = '.pdf'
        elif actual_bill.headers['content-type'] == 'image/png':
            extn = '.png'
        elif actual_bill.headers['content-type'] != 'image/jpeg':
            print("Bill not of jpg and pdf type. User {}, billNo: {}, content-type: {}".format(
                user_id,
                unique_bill_key.encode(
                    'utf-8'), str(actual_bill.headers['content-type'])))
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


def process_user_bills(bills, status, user_id):
    if status is not 200:
        print("Response not 200. response: {}, Status: {}, userID: {}".format(bills, status,
                                                                              str(user_id)))
    else:
        path = program_folder_path + str(user_id) + '/'
        delete_dir(path)
        make_dir_from_path(path)
        print("Creating user folder and saving json")
        with io.open(path + user_id + '.json', 'w', encoding='utf8') as outfile:
            outfile.write(to_unicode(bills))
        bills_json = json.loads(bills)
        if len(bills_json["bills"]) == 0:
            print("No bills found for mentioned date range")
        for bill in bills_json["bills"]:
            process_bill(str(user_id), path, bill)


def process_user_cards(user_id, card_id):
    try:
        print("Processing userID: {}".format(user_id))
        url = api_url + '&userID=' + user_id + '&count=100&cardID=' + card_id + '&dateRange.fromDateYYYYmmDD=' + uploaded_at_start_date + '&dateRange.toDateYYYYmmDD=' + uploaded_at_end_date
        bills, status = request(method='GET',
                                url=url)
        process_user_bills(bills, status, user_id)
    except Exception as e:
        print("Error while processing user: {}".format(str(user_id)))
        logging.exception(
            "Error while processing User: " + str(user_id))


def process_users_cards():
    with open(list_of_user_cards) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_user_cards(row['userid'], row['cardid'])


def main():  # pragma: no cover
    process_users_cards()
    print("Done !!!")


if __name__ == '__main__':  # pragma: no cover
    main()
