# Insta -k
A Simple Script Written in Python by : **khaled ait miloud (@khaled_aitmiloud)**
This Script will find random users  based by your custom tags to follow or send a message.

## Deployment
### Pre-requisits:
- Install Python3 (Python 3.7.3) with pip3
### Quick Setup
- Clone the repository: `git clone https://github.com/Over-k/insta.git`
- Install pip requirements: `pip3 install -r requirements.txt`
### Configuration
- After simply downloading this repository, open **script.py** , you’ll have to change some lines.
- 1. Path to your chrome profile or you can open chrome and type: "chrome://version/" on URL
`chrome_options.add_argument(r"--user-data-dir=C:\Users\Name\AppData\Local\Google\Chrome\User Data\Default")`
- 2. download from https://chromedriver.chromium.org/downloads, If you have correctly downloaded Chromedriver, change the path to your chromedriver file.
 `chrome_driver_exe_path = abspath("C:\Python\chromedriver.exe")`
- These two lines are designed to save your authenticated on Instagram.
 - Basically change `python3 script.py -u your_username -p your_password` to your Instagram credentials.

### Run the program
- Example: `python3 script.py -u your_username -p your_password  -t python -sc 30 -img True`
- `-h`: to display help menu
- `-u`: your own instagram username
- `-p`: your own instagram password
- `-t`: to specify hashtags (REQUIRED) `-t tag1 tag2 tag3`
- `-sc`: to specify number of scrolling (default:10)
- `-s`: if want send messages (default: False)
- `-f`:  if want following users (default: False)
- `-save`: if want save your users (default: True)
- `-img`: if want block load pictures (default: False)
- Simply run the command line below in a terminal:`python3 script.py -t dart ruby assembly`
#### Disclaimer
This project is fully implemented for educational purposes only and I am not responsible by any means for any misuse.
