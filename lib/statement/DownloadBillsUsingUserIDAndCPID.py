import csv
import json
import urllib2

from lib.utils.folder_util import make_dir_from_path
from lib.utils.request_util import request

token = 'MldCTzVWOTB5WS9wVC9CcklYbjA5bHdzY1d0cnF0S2doVVlMd1ZoWVlKQ2lHSkpsOkFRSGlxZnFIT05OcmZCT3VqRUcweHRQL1VtVWlaM3RnUlZiUkZlQjhwckw0U0tBcG04WW1HQW5LMThteG85dFVJd3h0bmFzRFRTTDhmdU84ckduRkx3alE5ZitJTk1NR1VaVlRUMWIybVhYOVdHU2E5T1FIQkVkVWdvdlNHcDFxWVVFaTY4NzdlOXlEVG5TMGVBVmZSTURHdjRLUmdQRT0='

api_url = 'https://api.gw.zetapay.in/zeta.in/biller/1.0/userBills?token=' + token


def get_bill(zeta_user_id, cardprogram_id):
    url = api_url + '&userID=' + zeta_user_id + '&cardProgramID=' + cardprogram_id
    bills, status_code = request(method='GET', url=url)
    return bills


def process_bill(bill, email):
    count = 1
    for billUrl in bill["billUrls"]:
        actual_bill = urllib2.urlopen(billUrl)
        extn = '.jpg'
        if actual_bill.headers['content-type'] == 'application/pdf':
            extn = '.pdf'
        elif actual_bill.headers['content-type'] == 'image/png':
            extn = '.png'
        elif actual_bill.headers['content-type'] != 'image/jpeg':
            print "Bill not of jpg and pdf type.  billNo: {}, content-type: {}".format(

                bill['claimId'], str(actual_bill.headers['content-type']))
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


with open('/Users/rahil.r/Documents/tmp/oyo_fuel.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        zeta_user_id = row[0]
        email = row[1]
        cardprogram_id = row[2]
        print(zeta_user_id + " " + email + " " + cardprogram_id)
        bills = json.loads(get_bill(zeta_user_id, cardprogram_id))
        folder_path = '/Users/rahil.r/Documents/tmp/oyo_users_fuel' + '/' + email
        try:
            make_dir_from_path(folder_path)
        except Exception as e:
            print "Error while processing user: {}".format(str(zeta_user_id))
        for bill in bills['bills']:
            process_bill(bill, email)
