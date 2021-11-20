
# CRO-DeFi-Warner

2 Options to use this at the moment:
* Run with python file
* Run with .exe file

Notifications was only tested for Windows 10. Not sure if it works for other OS like unix or mac, it technically should work. 

## Option 1: .exe File
1. Download .exe file and config file
2. Place it in a folder
3. Update [config.json](config.json) file: 
	- Edit Validator Address ([find it here](https://crypto.org/explorer/validators), it's called operator address)
	- Edit Account Address
	- Set Total Rewards Limit (set to 0 if not needed)
4. Run file manually once
5. Schedule using any task scheduler (Windows Task Scheduler, cron, etc.)

## Option 2: Python File
Python version: >3.9 (maybe works with other versions too..., tested on 3.9.9)
Prerequisites:

    pip install notify-py requests

Update [config.json](config.json) file: 
- Edit Validator Address ([find it here](https://crypto.org/explorer/validators), it's called operator address)
- Edit Account Address
- Set Total Rewards Limit (set to 0 if not needed)

Run:
 1. Place python file and config file in same folder
 2. Run using python cro-defi-warner.py
 3. Schedule using any task scheduler (Windows Task Scheduler, cron, etc.)


