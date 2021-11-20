import sys
import requests
import json
import os.path
from notifypy import Notify

def convertToCRO(number):
    return round(number/100000000, 4)

def notification(title, message):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send()

#LOAD SETTINGS
if os.path.isfile("config.json"):
    with open("config.json") as f:
        settings = json.load(f)
    if settings["validator"].startswith("cro"):
        validator = settings["validator"]
    if settings["account"].startswith("cro"):
        account = settings["account"]
    totalrewardslimit = settings["totalrewards"]
else:
    sys.exit(1)

validator_file = validator + ".json"
account_file = account + ".json"

#CHECK IF FILE EXISTS / FIRST START
if not os.path.isfile(validator_file):
    validator_response = requests.get("https://crypto.org/explorer/api/v1/validators/" + validator) 
    validator_new = json.loads(validator_response.text)
    with open(validator_file, 'w') as f:
        json.dump(validator_new, f)

if not os.path.isfile(account_file):
    account_response = requests.get("https://crypto.org/explorer/api/v1/accounts/" + account)
    account_new = json.loads(account_response.text)
    with open(account_file, 'w') as f:
        json.dump(account_new, f)

#GET NEW DATA
validator_response = requests.get("https://crypto.org/explorer/api/v1/validators/" + validator)
validator_new = json.loads(validator_response.text)
with open(validator_file) as f:
    validator_old = json.load(f)

account_response = requests.get("https://crypto.org/explorer/api/v1/accounts/" + account)
account_new = json.loads(account_response.text)
with open(account_file) as f:
    account_old = json.load(f)

#COMPARE WITH OLD
if not validator_new["result"]["commissionRate"] == validator_old["result"]["commissionRate"]:
    commission_new = float(validator_new["result"]["commissionRate"])*100
    commission_old = float(validator_old["result"]["commissionRate"])*100
    if commission_new > commission_old:
        warning = "Commission was changed \nNew Rate: " + str(commission_new) + "% / Old Rate: " + str(commission_old) + "%"
        print("WARNING: " + warning)
        notification("CRO DeFi Earn - Warning", warning)

if validator_new["result"]["jailed"]:
    warning = "Validator '" + validator_new["result"]["moniker"] + "' is jailed"
    print("WARNING: " + warning)
    notification("CRO DeFi Earn - Warning", warning)
        
if not totalrewardslimit == 0:
    if convertToCRO(float(account_new["result"]["totalRewards"][0]["amount"])) > totalrewardslimit:
        message = "Total Rewards Limit reached \nCurrent Total Rewards: " + str(convertToCRO(float(account_old["result"]["totalRewards"][0]["amount"]))) + " CRO \nLimit: " + str(totalrewardslimit) + " CRO"
        print("INFO: " + message) 
        notification("CRO DeFi Earn - Info", message)
        
#SAVE NEW TO OLD
with open(validator_file, 'w') as f:
    json.dump(validator_new, f)   
with open(account_file, 'w') as f:
    json.dump(account_new, f)

# print("****** VALIDATOR INFO ******")
# print("Jailed: " + str(validator_new["result"]["jailed"]))
# print("Bonded Status: " + validator_new["result"]["status"])
# commission = float(validator_new["result"]["commissionRate"])*100
# print("Current Comission: " + str(commission) + "%")
# print("")
# print("")

# print("****** WALLET INFO ******")
# print("Unused Balance: " + str(convertToCRO(float(account_new["result"]["balance"][0]["amount"]))))
# print("Total Rewards: " + str(convertToCRO(float(account_new["result"]["totalRewards"][0]["amount"]))))
# print("Total Bonded Balance: " + str(convertToCRO(float(account_new["result"]["bondedBalance"][0]["amount"]))))
# print("Total Balance: " + str(convertToCRO(float(account_new["result"]["totalBalance"][0]["amount"]))))