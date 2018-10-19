import json

json_string = {'id': 2291638, 'name': 'jane doe', 'email': 'N/A', 'companyid': 9682, 'phonenumber': '9035305007',
               'createdat': 'createdat', 'updatedat': 'updatedat', 'external_companycode': None,
               'external_empcode': None,
               'external_paygroupcode': None, 'employee_start_date': None, 'attributes': {b'empid': b'22.0'},
               'CRN': 'N/A',
               'pan': '344455556565', 'kyc_updated_at': 'kyc_updated_at', 'zeta_user_id': None,
               'identifier_list': 'PHONENUMBER', 'state': 'ACTIVE'}

# json_dumped = str(json_string).encode().decode(encoding='utf-8', errors='strict')
# for key in json_string:
#    print(json_string[key] is json)
# print(str(json_string).encode().decode(encoding='utf-8', errors='strict'))
# jjson=json.loads(str(json_string), encoding='utf-8')
# print(jjson)


problem_json = "{b'empid': b'22.0'}"
print(json.loads(problem_json.decode('utf-8')))
