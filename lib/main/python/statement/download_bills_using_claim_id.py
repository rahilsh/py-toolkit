import json
import urllib2

from lib.main.python.utils.request_util import request

token = ''

api_url = 'https://localhost:8080/getBill?token=' + token

claimIds = ['9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805742102-o3V4']


def get_bill(claim_id):
    url = api_url + '&claimID=' + claim_id
    bill, status_code = request(method='GET', url=url)
    process_bill(json.loads(bill))


def process_bill(bill):
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
                '/Users/rahil.r/Documents/tmp/' + bill['claimId'].split('_')[1] + str(
                    count_suffix) + extn,
                'wb') as output:
            output.write(actual_bill.read())
        count = count + 1


for claimId in claimIds:
    print 'Processing: ' + claimId
    get_bill(claimId)

print 'Done !!!'
