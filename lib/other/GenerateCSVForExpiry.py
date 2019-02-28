import psycopg2

print "Enter ledger DB username"
username = raw_input()

print "Enter ledger DB password"
password = raw_input()
try:
    # conn = psycopg2.connect("dbname='reporting' user='{}' host='10.19.2.148' password='{}'".format(username, password))
    # conn = psycopg2.connect("dbname='ledger' user='{}' host='10.1.5.1' port='5442' password='{}'".format(username, password))
    conn = psycopg2.connect(
        "dbname='reporting' user='{}' host='10.19.2.148' port='5432' password='{}'".format(username, password))
except:
    print "unable to connect to the database"

cur = conn.cursor()

f = open('cashless_expiry_20-Jan-2019_1.csv', 'w')

# query = "select ledgerid as from_ledger, (2974292896711714503) as to_ledger, balanceafter as value, currency from get_ledger_balance_before_date('2018-01-01') where balanceafter > 0;"

# query = "select ledgerid as from_ledger, (3826931177588844679) as to_ledger, balanceafter as value, currency from get_ledger_balance_before_date_for_cp('2018-04-01','af195eef-a4a4-4166-bab2-fc5d472a4d34') where balanceafter > 0;"

# cur.execute(query)
# rows = cur.fetchall()


query = "select ledgerid as from_ledger, (8917698968981900400) as to_ledger, balanceafter as value, currency from get_ledger_balance_before_date_for_cp('2019-02-21','774e0f1c-029b-4607-890e-25387e8d9df1') where balanceafter > 0";
cur.execute(query)

rows = cur.fetchall()

query = "select ledgerid as from_ledger, (8917698968981900400) as to_ledger, balanceafter as value, currency from get_ledger_balance_before_date_for_cp('2019-02-21','376e9ae5-73ff-4349-810c-cea3f3ee5a03') where balanceafter > 0";
cur.execute(query)

for i in cur.fetchall():
    rows.append(i)

for row in rows:
    f.write("{},{},{},{}\n".format(row[0], row[1], row[2], row[3]))
