import json
import urllib2

from lib.utils.request_util import request

token = 'MldCTzVWOTB5WS9wVC9CcklYbjA5bHdzY1d0cnF0S2doVVlMd1ZoWVlKQ2lHSkpsOkFRSGlxZnFIT05OcmZCT3VqRUcweHRQL1VtVWlaM3RnUlZiUkZlQjhwckw0U0tBcG04WW1HQW5LMThteG85dFVJd3h0bmFzRFRTTDhmdU84ckduRkx3alE5ZitJTk1NR1VaVlRUMWIybVhYOVdHU2E5T1FIQkVkVWdvdlNHcDFxWVVFaTY4NzdlOXlEVG5TMGVBVmZSTURHdjRLUmdQRT0='

api_url = 'https://api.gw.zetapay.in/zeta.in/biller/1.0/getBill?token=' + token

claimIds = ['9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805742102-o3V4','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805709913-k47a','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805613272-dtMk','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805549194-DOom','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544806191006-3KZe','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544806120049-vwZl','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805767471-tiGS','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1551682268712-EEQ6','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805192448-TCBF','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541153289352-1Sfx','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541153212524-5ssp','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541153142829-d0zL','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541151915461-TYMU','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535798479508-ZGrH','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535798442153-JJLM','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535798330696-OPNO','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535799013398-Pwf7','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535798516155-Nb3D','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535798593830-f6lU','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1535799045973-WEuJ','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1542000103391-0BzT','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543980458538-GArD','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543981731582-9TVs','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543981459407-ODuG','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543981258882-MOO8','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536391011906-ZQ3e','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536391281324-o9hV','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1539448727689-WbiA','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1539448597679-n3b1','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1539448562503-6Mdw','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541923036497-S9tB','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1541922360302-DMZE','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536391181107-I4LT','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536391073414-Zz6k','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536291950292-XNe9','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536291889893-jCP3','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536291704734-6Eju','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536291606632-gq2J','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536289458577-YKtm','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536289119857-QPmH','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1536289021958-v8Xq','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543945285334-ASf7','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543945014941-ee33','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543944940075-RyYF','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1543944897726-iU1g','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1551866796224-578t','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1550290352054-mLqt','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1550306374612-ZJAM','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1550306297858-aIIO','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1551866799555-C8BE','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1551866641506-v3tF','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1552453119254-xvdP','9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1546764209114-2KiB']


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
                '/Users/rahil.r/Documents/tmp/oyo_fuel' + '/' + bill['claimId'].split('_')[1] + str(
                    count_suffix) + extn,
                'wb') as output:
            output.write(actual_bill.read())
        count = count + 1


for claimId in claimIds:
    print 'Processing: ' + claimId
    get_bill(claimId)

print 'Done !!!'
