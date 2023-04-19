import numpy as np
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pymysql
import struct
import datetime
import time
df_columns = ('code', 'date', 'orient',
              'v1', 'v2', 'v3', 'f',
              'sp', 'jm', 'bad')

comp_mark_value = {
    'v1':1<<3,
    'v2':1<<2,
    'v3':1<<1,
    'f':1
}

def post_marks_to_sql(rq):
    """
        постинг в SQL таблицу
        """
    obs_code = str(rq['code']).upper()
    date0 = int(rq['date0'])
    date1 = int(rq['date1'])
    marks_action = int(rq['action'])
    vector_comp = str(rq['comp']).lower()
    freq = str(rq['freq']).lower()

    if freq == 'min':
        tick = 60
        table_name = os.getenv('SQL_TABLE_MIN')
    else:
        tick = 1
        table_name = os.getenv('SQL_TABLE_SEC')

    # создаем массив меток времени, где нужно ввести пометки
    edit_min_range = np.arange(date0, date1+1, tick)

    try:
        conn = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                               user=os.getenv('SQL_USER'),
                               passwd=os.getenv('SQL_PSW'),
                               db=os.getenv('SQL_DB'),
                               charset='utf8mb4', autocommit=False)
        cur = conn.cursor()

        # бежим по каждой строке sql таблицы, строка=час
        date0_round = date0 // 3600 * 3600
        for dt_hour in np.arange(date0_round, date1 + 1, 60 * 60):  # for every hour
            request_to_db = "SELECT date, bad FROM %s WHERE code='%s' " \
                            "AND date=%i" % (table_name, obs_code, dt_hour)

            cur.execute(request_to_db)
            respond = cur.fetchall()[0]
            sql_date, sql_bad = respond

            # если это первая запись
            if sql_bad is None:
                if freq == 'min':
                    bad_array = np.zeros(60).astype(int)
                else:
                    bad_array = np.zeros(3600).astype(int)

            # если нужно обновить строку
            else:
                fmt = '>B'
                bad_array = np.array(list(struct.iter_unpack(fmt, sql_bad)),
                                     dtype=np.int).squeeze()

            # обновляем bad_array
            for i, dt_min in enumerate(np.arange(dt_hour, dt_hour + (60 * 60), tick)):
                if dt_min in edit_min_range:
                    if marks_action:
                        bad_array[i] |= comp_mark_value[vector_comp]
                    else:
                        bad_array[i] &= ~comp_mark_value[vector_comp]

            # постим в таблицу
            sql_upd_request = """UPDATE %s SET """ % table_name + """bad=%s""" \
                              + """ WHERE code='%s' AND date=%i""" % (obs_code, dt_hour)
            insert_array_byte = struct.pack('>%sB' % len(bad_array), *bad_array)
            insert_tuple = (insert_array_byte)
            cur.execute(sql_upd_request, insert_tuple)
            conn.commit()
            conn.close()
            return 0
    except Exception as e:
        print(e)
        return 1





def get_marks_from_sql(rq):
    obs_code = str(rq['code']).upper()
    # obs_code = 'IRT'
    date = int(rq['date'])
    conn = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                           user=os.getenv('SQL_USER'),
                           passwd=os.getenv('SQL_PSW'),
                           db=os.getenv('SQL_DB'),
                           charset='utf8mb4', )
    cur = conn.cursor()
    request_to_db = "SELECT * FROM %s WHERE code='%s' " \
                    "AND date=%i AND " % (os.getenv('SQL_TABLE'), obs_code, date)

    cur.execute(request_to_db)
    respond = cur.fetchall()[0]
    conn.close()
    # 0    1    2    3   4    5    6    7    8     9
    # c    d    o    v1  v2  v3   f     sp   jm    bad

    idx = 9
    print('idx:', idx)

    # unpack
    fmt = '>B'

    hour_arr = np.array(list(struct.iter_unpack(fmt, respond[idx])),
                        dtype=np.int).squeeze()
    print(hour_arr)
    print(len(hour_arr))

    # pack
    buf = struct.pack('>%sB' % len(hour_arr), *hour_arr)  # same as respond[idx]

    if buf == respond[idx]:
        print('success')
    else:
        print('fail')
    print('--------------------------------------')
