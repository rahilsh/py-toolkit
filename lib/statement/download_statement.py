import csv
import io
import json
import logging
import urllib2

from lib.utils.folder_util import delete_dir
from lib.utils.folder_util import make_dir_from_path
from lib.utils.image_util import convert_pdf_to_img
from lib.utils.request_util import request
from lib.utils.unicode_util import to_unicode

# Update below five properties
quarter_folder = '/Users/rahil.r/Documents/tmp/practo/oct_dec/'
program_type = 'asset'
list_of_user_cards = quarter_folder + program_type + '.csv'
program_folder_path = quarter_folder + program_type + '/'
# keep it a day extra in both below dates
uploaded_at_start_date = '20180930'
uploaded_at_end_date = '20190101'

token = 'Smk3bUFlQVlyZHZrWDNTNTVuZE1tdVgyNGZQMHFXUXlDckhzdDdBWCtxdlpnRCs5OkFRSGdaaHBmTktubXBGcFVQa1ZBMFUyaGZlZ1F5dDNMK2Irc2RLakVrSld1M2xMc1loejYxbDdTU2pHZ3BvZTh6ZTM3T2tBUUpXTFNhaXN5S1dxMjkxcTZFMldtbnJxcFNYUFpWNmUxRjVhNHp3Zmc4SkxMcitna2N6NGhSWTIybkMvQVg0c0l1Q3ZYQmtrKzErL0xqV08rVFNMUW9xdz0='

api_url = 'https://api.gw.zetapay.in/zeta.in/biller/1.0/userBills?token=' + token


def process_bill(user_id, path, bill):
    unique_bill_key = ''
    if 'billNumber' in bill['attrs']:
        unique_bill_key = bill['attrs']['billNumber']
    if unique_bill_key == '':
        # print "Bill No not present, hence using claimID"
        unique_bill_key = bill['claimId']
    unique_bill_key = unique_bill_key.replace('/', '_')
    # if unique_bill_key in {'a1478'}:
    #     print("skipping as it is already processed")
    #     continue
    # if unique_bill_key in {'10ika06816687555'}:
    #     print("skipping as pdf is pass protected")
    #     continue
    print "Processing bill no: {}".format(unique_bill_key.encode('utf-8'))
    # if bill['uploadedAt'] is not None and (
    #         bill['uploadedAt'] < uploaded_at_start_date or bill[
    #     'uploadedAt'] > uploaded_at_end_date):
    #     print("skipping as bill is out of mentioned time period")
    #     return
    # if bill['state'] == 'PAID' or bill['state'] == 'PARTIALLY_PAID' or bill[
    #     'state'] == 'APPROVED' or bill['state'] == 'UNPAID':
    # print "Bill is Approved"
    bills_folder_path = path + 'bills/' + unique_bill_key
    make_dir_from_path(bills_folder_path)
    process_bill_urls(bill, bills_folder_path, unique_bill_key, user_id)
    # else:
    #     print "Skipping bill as it is not approved. BillNo: {}".format(
    #         unique_bill_key.encode('utf-8'))


def process_bill_urls(bill, bills_folder_path, unique_bill_key, user_id):
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
                user_id,
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


def process_user_bills(bills, status, user_id):
    if status is not 200:
        print "Response not 200. response: {}, Status: {}, userID: {}".format(bills, status,
                                                                              str(user_id))
    else:
        path = program_folder_path + str(user_id) + '/'
        delete_dir(path)
        make_dir_from_path(path)
        print "Creating user folder and saving json"
        with io.open(path + user_id + '.json', 'w', encoding='utf8') as outfile:
            outfile.write(to_unicode(bills))
        bills_json = json.loads(bills)
        if len(bills_json["bills"]) == 0:
            print "No bills found for mentioned date range"
        for bill in bills_json["bills"]:
            process_bill(str(user_id), path, bill)


def process_user_cards(user_id, card_id):
    try:
        print "Processing userID: {}".format(user_id)
        url = api_url + '&userID=' + user_id + '&count=100&cardID=' + card_id + '&dateRange.fromDateYYYYmmDD=' + uploaded_at_start_date + '&dateRange.toDateYYYYmmDD=' + uploaded_at_end_date
        bills, status = request(method='GET',
                                url=url)
        process_user_bills(bills, status, user_id)
    except Exception as e:
        print "Error while processing user: {}".format(str(user_id))
        logging.exception(
            "Error while processing User: " + str(user_id))


def process_users_cards():
    with open(list_of_user_cards) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_user_cards(row['userid'], row['cardid'])


def main():
    process_users_cards()
    print "Done !!!"


if __name__ == '__main__':
    main()
