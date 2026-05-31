import csv
import json
from urllib.request import urlopen

from py_toolkit.utils.folder_util import make_dir_from_path
from py_toolkit.utils.request_util import request

token = ''

api_url = 'https://localhost/userBills?token=' + token


def get_bill(user_id, cardprogram_id):
    url = api_url + '&userID=' + user_id + '&cardProgramID=' + cardprogram_id
    bills, status_code = request(method='GET', url=url)
    return bills


def process_bill(bill, email, folder_path):
    count = 1
    for billUrl in bill["billUrls"]:
        actual_bill = urlopen(billUrl)
        extn = '.jpg'
        if actual_bill.headers['content-type'] == 'application/pdf':
            extn = '.pdf'
        elif actual_bill.headers['content-type'] == 'image/png':
            extn = '.png'
        elif actual_bill.headers['content-type'] != 'image/jpeg':
            print("Bill not of jpg and pdf type.  billNo: {}, content-type: {}".format(

                bill['claimId'], str(actual_bill.headers['content-type'])))
        if len(bill["billUrls"]) == 1:
            count_suffix = ''
        else:
            count_suffix = '_' + str(count)
        with open(
                folder_path + '/' + bill['claimId'].split('_')[
                    1] + str(
                    count_suffix) + extn,
                'wb') as output:
            output.write(actual_bill.read())
        count = count + 1


def main():  # pragma: no cover
    with open('/Users/rahil.r/Documents/tmp/test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            user_id = row[0]
            email = row[1]
            cardprogram_id = row[2]
            print(user_id + " " + email + " " + cardprogram_id)
            bills = json.loads(get_bill(user_id, cardprogram_id))
            folder_path = '/Users/rahil.r/Documents/tmp/test' + '/' + email
            try:
                make_dir_from_path(folder_path)
            except Exception:
                print("Error while processing user: {}".format(str(user_id)))
            for bill in bills['bills']:
                process_bill(bill, email, folder_path)


if __name__ == '__main__':  # pragma: no cover
    main()
