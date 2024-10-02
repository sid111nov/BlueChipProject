from mongo_connection import getconnection2collection
from djia_companies import DJIA_LIST

income_connection = getconnection2collection("stockdata","income_stmt")
balancesheet_connection = getconnection2collection("stockdata","balancesheet")
cashflow_connection = getconnection2collection("stockdata","cashflow")

ticker ="MCD"

inc_result = income_connection.find_one({"ticker":ticker})
bs_result = balancesheet_connection.find_one({"ticker":ticker})
cf_result = cashflow_connection.find_one({"ticker":ticker})

print(inc_result["income_stmt"])
print(bs_result["balance_sheet"])
print(bs_result["cashflow_stmt"])