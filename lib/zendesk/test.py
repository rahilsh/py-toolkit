# from Backfill import request
#
# querystring = {"mobileNumber": "%2B917600216682",
#                "token": "QnQvMWJhVk9qUG5YK3NvbVlXd3kwQ2FxN2RaMzZsUy9IYlVFSFNjL09GSmZqNEFOOkFRRWRCbzc5MlU1eHkxZ05aY21ac0l1ZTVpZVk5ZW1pZ1VaRCtLL1cweE81TC9KMjJxTmNYRXhVTUNCSTBvY0k0RURSdHIvOUlYVU1GNElneFE2OWk1TUdYcGo5NWVlamtsTDNhVXVzUHhLSE9HT2hCSW55eksyZ1BDT1Y5U3BBUzhORkR2dWlQNDQxam56Q3pyWExJL1orcWdnPQ=="}
# response, code = request(method="GET",
#                          url="https://api.gw.zetapay.in:443/zeta.in/zetauser/1.0/getProfileByMobile",
#                          params=querystring)
#
# print "{},{}".format(response, code)
import json
import asyncore

response = '{"bankAccounts":[],"dob":"19920607","kycDob":"","gender":"male","kycDone":false,"trustedContacts":[],"attrs":{"corpID":"4374","isCorpUser":"true","isPassphraseSet":"true","isSecondFactorSet":"true","deferCashCardCreation":"true"},"userSalt":"B8OUqPsjygDTneljfduraA\u003d\u003d","isPassphraseSet":true,"isSecondFactorSet":true,"roles":[],"createdAt":1518454193708,"userType":"REGULAR","userID":1514713,"mobileNumber":"+918486055157","name":{"firstName":"Priyankush","lastName":"Bora"},"kycName":"Priyankush Bora","addresses":[{"tag":"work","line1":"3A, 3rd Floor, Ganapati Enclave","line2":"G.S. Road, Bora Service","city":"Guwahati","state":"Assam","country":"India","postalCode":"781007"},{"tag":"home","line1":"House no. 65","line2":"Kotohaboria Gaon","city":"Jorhat","state":"Assam","country":"India","postalCode":"785010"}],"emailList":[{"email":"priyankush.bora@quickheal.co.in","isVerified":true,"unsubscribed":false}],"phoneNumbers":[{"phoneNumber":"+918486055157","isVerified":true}],"businessIDs":[],"userDocs":[],"userState":"CREATED","headers":{}}'
if "corpID" in json.loads(response)["attrs"]:
    print "true"
