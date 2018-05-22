# Copyright © 2018 Stanislav Hnatiuk.  All rights reserved.

#!/usr/bin/env python3

import sys
import psycopg2
import base64
import struct
import datetime
import json


def connection():
    '''Создать соединение с базой данных ИИОН. Возвращает connection и cursor.'''
    with open('.connection.json', 'rt') as file:
        param = json.loads(file.read())
        conn = psycopg2.connect(**param)
        cur = conn.cursor()
        return conn, cur


def get_struct(conn, cur):
    '''Получить структуру БД.'''
    try:
        cur.execute("""SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='public'""")
        for table in cur.fetchall():
            print('{}:'.format(table[2]))
            cur.execute("""SELECT * FROM {table} LIMIT 0""".format(table=table[2]))
            for column in cur.description:
                print('|{:<15}:{}'.format(column[0], column[1]))
            print('\n')
    except psycopg2.Error as e:
        print(str(e))


def get_sfile(conn, cur, date=None):
    '''Получить S-файлы из БД.'''
    try:
        table = 's_new_file'
        if date:
            condition = " WHERE DATE(date)='{}'".format(date)
        else:
            condition = ''
        cur.execute("""SELECT date, session, acf1_arr FROM {table}{condition} ORDER BY date""".format(table=table, condition=condition))
        downloaded = cur.fetchall()
        for i, row in enumerate(downloaded):
            print(i, row[0])
            buf = base64.b64decode(row[2])
            path = 'data/{}'.format(row[0].strftime('%d%m%y.%H%M'))
            with open(path, 'wb') as file:
                file.write(buf)
                # print(len(buf))
                # break
    except psycopg2.Error as e:
        print(str(e))


def get_dates(conn, cur):
    '''Получить даты из БД.'''
    try:
        table = 's_new_file'
        cur.execute("""SELECT DISTINCT EXTRACT(year from date) as date FROM {table} ORDER BY date""".format(table=table)) #WHERE DATE(date)>'2017-12-01' 
        downloaded = cur.fetchall()
        for i, row in enumerate(downloaded):
            print('{}:\t{}'.format(i, row[0]))
    except psycopg2.Error as e:
        print(str(e))
