import sqlite3
conobj=sqlite3.connect(database="bank.sqlite")          #database=bank.sqlite
curobj=conobj.cursor()

try:        #table name=users
    table_users='''create table users(users_acno integer primary key autoincrement,     
    users_name text,users_pass text,users_mob text,users_email text,
    users_bal float, users_adhar text,users_opendate date)
'''
            #table name=txn
    table_txn='''create table txn(txn_id integer primary key autoincrement,             
    txn_acno int,txn_type text,txn_amt float,txn_bal float,
    txn_date text)
'''

    curobj.execute(table_users)
    curobj.execute(table_txn)
    print("tables created")
except Exception as e :
    print(e)        #table user already exists 
finally:
    conobj.close 

    