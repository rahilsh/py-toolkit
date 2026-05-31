import psycopg2

username = 'postgres'
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
        print("unable to connect to the database: {}".format(str(e)))


if __name__ == '__main__':  # pragma: no cover
    print(execute('select * from test'))
