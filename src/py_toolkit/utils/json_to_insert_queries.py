# coding=utf-8

if __name__ == '__main__':  # pragma: no cover
    employees = {
                    "id": "1",
                    "name": "a"
                }, {
                    "id": "2",
                    "name": "b"
                }

    for employee in employees:
        print("insert into employee (id, name)"
              " values ('{}','{}');".format(employee.get('id'),
                                            str(employee.get('name'))))
