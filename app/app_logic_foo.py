import numpy as np
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pymysql

df_columns = ('code', 'date', 'orient',
              'v1', 'v2', 'v3', 'f',
              'sp', 'jm', 'bad')


def post_marks_to_sql(rq):
    """
        постинг в SQL таблицу
        """
    obs_code = str(rq['code']).upper()
    # obs_code = 'IRT'
    date = int(rq['time'])
    orient = str(rq['orient']).upper()

    """
    floatlist = [random.random() for _ in range(10**5)]
    buf = struct.pack('%sf' % len(floatlist), *floatlist)
    """

    try:
        conn = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                               user=os.getenv('SQL_USER'),
                               passwd=os.getenv('SQL_PSW'),
                               db=os.getenv('SQL_DB'),
                               charset='utf8mb4', )
        cur = conn.cursor()

        request_to_db = "SELECT * FROM %s WHERE code='%s' " \
                        "AND date=%i AND orient=%s" % (os.getenv('SQL_TABLE'), obs_code, date, orient)

        cur.execute(request_to_db)
        respond = cur.fetchall()
        # если это первая запись
        if len(respond) == 0:
            query = """ INSERT INTO """ + str(os.getenv('SQL_TABLE')) + """ 
                                (code, date, orient, v1, v2, v3, f, sp, jm, bad) 
                                VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)"""
            insert_tuple = (obs_code, date, orient, date1, filename, md5_hash, ucount, filesize)

            cur.execute(query, insert_tuple)
            conn.commit()
            conn.close()
            return 0


        # если нужно обновить строку
        else:
            sql_upd_request = """UPDATE %s SET """ + str(os.getenv('SQL_TABLE')) + """ 
                                            (code, date, orient, v1, v2, v3, f, sp, jm, bad) 
                                            VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)"""\
                              + """ WHERE code='%s' AND date=%i AND orient=%s"""% (obs_code, date, orient)

            insert_tuple = (obs_code, date, orient, date1, filename, md5_hash, ucount, filesize)
            cur.execute(sql_upd_request, insert_tuple)
            conn.commit()
            conn.close()
            return 0




    except Exception as E:
        print(E)
        return 1