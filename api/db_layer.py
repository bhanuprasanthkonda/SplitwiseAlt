import sqlite3
from sqlite3 import Error
from uuid import uuid1
from dataTypes import *


class DatabaseLayer:
    def __init__(self):
        self.__DATABASE_NAME = "test.db"
        self.__connection = None
        self.__connection = sqlite3.connect(self.__DATABASE_NAME)
        self.__check_tables()

    def __del__(self):
        self.__connection.close()

    # checks if the tables are present in the db. if not, will create them
    def __check_tables(self):
        # users table
        conn = self.__connection
        c = conn.cursor()
        try:
            c.execute('''select * from users''')
        except Error:
            c = conn.cursor()
            c.execute("""create table users(
                        uuid text,
                        loginId text,
                        password text,
                        PRIMARY KEY(loginId))""")
            conn.commit()

        # transactions table
        c = conn.cursor()
        try:
            c.execute('''select * from transactions''')
        except Error:
            c = conn.cursor()
            c.execute("""create table transactions(
                                sender_id text,
                                receiver_id text,
                                currency text,
                                amount NUMERIC,
                                create_time DATETIME)""")
            conn.commit()

    # generates uuid
    # added the user to the users table
    # returns the uuid of the user
    async def signup(self, rd: User_cred):
        conn = self.__connection
        c = conn.cursor()
        u = str(uuid1())
        try:
            c.execute(f"""Insert into users(uuid, loginId, password) values ('{u}', '{rd.loginId}', '{rd.password}')""")
            conn.commit()
        except Error as e:
            return {"Error": str(e)}
        return {"Success": u}

    # checks if the loginId and password matches with a row in the users table
    async def login(self, ld: User_cred):
        conn = self.__connection
        c = conn.cursor()
        result = []
        try:
            c.execute(f"select uuid from users where loginId = '{ld.loginId}' and password = '{ld.password}'")
            result = c.fetchone()
        except Error as e:
            return {"Error": str(e)}

        return {"Success": result[0]} if result else {"Error": "No such user"}

    # verifies the identity
    # checks if the users exists in the users table
    # add the transaction
    async def insert_transaction(self, td: Transaction_details):
        uuid = self.id_check(td.auth_details)
        r_id = self.user_exists(td.receiver)
        if await uuid and await r_id:
            conn = self.__connection
            c = conn.cursor()
            try:
                query = f"""Insert into transactions(sender_id,receiver_id,currency,amount,create_time) values 
                            ('{td.sender}', '{td.receiver}', '{td.curr}','{td.amount}','{td.time}')"""
                c.execute(query)
                conn.commit()
            except Error as e:
                return {"Error": str(e)}
            return {"Success": "Transaction added Successful"}
        else:
            return {"Error": f"Invalid {'sender id / uuid' if uuid else 'receiverId'}"}

    # returns all the users
    async def users(self):
        conn = self.__connection
        c = conn.cursor()
        try:
            c.execute("""select * from users""")
        except Error as e:
            return {"Error": str(e)}
        return {"Users": c.fetchall()}

    # return all the transactions
    async def all_transactions(self):
        conn = self.__connection
        c = conn.cursor()
        try:
            c.execute("""select * from transactions""")
        except Error as e:
            return {"Error": str(e)}
        return {"All Transactions": c.fetchall()}

    # validates the id by checking the loginId and uuid are from the same row of users
    async def id_check(self, auth: Auth_details):
        with self.__connection as conn:
            c = conn.cursor()
            query = f"select * from users where login = '{auth.loginId}' and uuid='{auth.uuidId}'"
            try:
                c.execute(query)
            except Error as e:
                return {"Error": str(e)}
            k = c.fetchall()
            return len(k) != 0

    # checks if the user exists in the users table
    async def user_exists(self, loginId):
        with self.__connection as conn:
            c = conn.cursor()
            query = f"select * from users where login = '{loginId}'"
            try:
                c.execute(query)
            except Error as e:
                return {"Error": str(e)}
            k = c.fetchall()
            return len(k) != 0

    # validates the user id
    # returns all the transactions of the user
    async def my_transactions(self, user_id):
        with self.__connection as conn:
            c = conn.cursor()
            query = f"select * from transactions where sender_id='{user_id}' or receiver_id ='{user_id}'"
            try:
                c.execute(query)
            except Error as e:
                return {"Error": str(e)}

            return c.fetchall()
