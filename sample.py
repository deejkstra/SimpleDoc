#!/usr/bin/python

import sys, json, time, datetime
import mysql.connector as mariadb

#
#   Database Handler
#

def connect():
    try:
        conn = mariadb.connect(user='root', password='', database='SimpleDoc')
        return conn.cursor()
    except Error as e:
        log(e)

def quick_fetch(query, data):

    try:
        conn = connect()
        conn.execute(query, data)
        result = conn.fetchall()
    except Error as e:
        log(e)
    finally:
        conn.close()
        return result

def quick_nofetch(query, data):
    try:
        conn = connect()
        conn.execute(query, data)
    except Error as e:
        log(e)
    finally:
        conn.close()

#
#   CRUD Handlers
#

def create(data):

    query = "
        INSERT INTO doc_data
        (title, doc_path) VALUES (%s, %s)
    "

    title = data['title']
    path = title + '.doc'

    arr = (title, path)

    create_file(path, data['doc'])
    quick_nofetch(query, arr)

def create_file(path, data):
    with open(str(path),'w') as fh:
        fh.write(data)

def read(data):

    query = "
        SELECT title, doc_path
        FROM doc_data
        WHERE id = %s
    "

    result = quick_fetch(query, data)
    title = result['title']
    path = result['doc_path']

    doc_data = read_file(path)

    # json
    return {"title":title, "data":doc_data}

def read_file(path):
    with open(path, '') as fh:
        content = fh.read()
    return content

def update(data):

    # TODO
    query = "
        UPDATE doc_data
        WHERE id = %d
    "

    quick_nofetch(query, data)

def update_file(path):
    return

def delete(data):
    return

#
#   Log
#

def log(msg):
    with open('python.log','a') as fh:
        fh.write(datetime.
                 datetime.
                 fromtimestamp(time.time()).
                 strftime('%Y-%m-%d %H:%M:%S'))
        fh.write(' ' + msg + '\n')

#
#   Application
#

try:
    lines = sys.argv
    op = lines[1]
    data = lines[2]

    operations = {
        'create' : create,
        'read' : read,
        'update' : update,
        'delete' : delete
    }

    result = operations[op](data)

    print result
except:
    print 'py_error'

sys.stdout.flush()

