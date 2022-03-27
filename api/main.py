from fastapi import FastAPI
from db_layer import DatabaseLayer
from dataTypes import *

app = FastAPI()

test_data = {}
transactions = []
uuids = {}

db_instance = DatabaseLayer()


@app.post("/signup")
async def signup(reg_details: User_cred):
    return await db_instance.signup(reg_details)


@app.post("/login")
async def login(login_details: User_cred):
    try:
        return await db_instance.login(login_details)
    except:
        return {"Error": "Internal Server Error"}


@app.post("/transaction")
async def transaction(td: Transaction_details):
    if td.sender == td.receiver:
        return {"Error": "Sender and Reciever can't be same"}

    return await db_instance.insert_transaction(td)


@app.get("/users")
async def all_users():
    return await db_instance.users()


@app.get("/alltransactions")
async def all_transactions():
    return await db_instance.all_transactions()


@app.post("/mytransactions")
async def all_transactions(auth: Auth_details):
    if await db_instance.id_check(auth):
        tran = await db_instance.my_transactions(auth.loginId)
        dic = {}
        for i in tran:
            try:
                dic[i[2]] += i[3] * (1 if i[0] == auth.loginId else -1)
            except KeyError:
                dic[i[2]] = i[3] * (1 if i[0] == auth.loginId else -1)
        return {"Amount": dic, "Transactions": tran}
    return {"Error": "User authentication fail"}
