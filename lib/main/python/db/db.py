import psycopg2

# print "Enter DB username"
# username = raw_input()
username = 'postgres'
# print "Enter DB password"
# password = raw_input()
password = ''


def execute(query):
    try:
        conn = psycopg2.connect(
            "dbname='postgres' user='{}' host='localhost' port='5432' password='{}'".format(username, password))
        cur = conn.cursor()
        query = "select id, name from test"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print "unable to connect to the database: {}".format(str(e))


print execute('select * from test')
