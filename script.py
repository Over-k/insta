from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import argparse
from time import *
import json
import re
from os.path import abspath
from os import path
from tabulate import tabulate
from s import main

# ┌────────────────────────┐
# |   Over-k               |
# └────────────────────────┘

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username',
                        dest="Username",
                        help="Your own Instagram username",
                        default="",
                        required=False)
    parser.add_argument('-p', '--password',
                        dest="Password",
                        help="Your own Instagram password",
                        default="",
                        required=False)
    parser.add_argument('-t', '--hashtags',
                        dest="Hashtags",
                        help="Hashtags Target",
                        nargs="+",
                        default=["python"],
                        required=True)
    parser.add_argument('-sc', '--scrolling',
                        dest="Scroll",
                        help="Number of scroll",
                        default=10,
                        required=False)
    parser.add_argument('-s', '--send_messages',
                        dest="Send",
                        help="Do you want send messages (True/False)",
                        default=False,
                        required=False)
    parser.add_argument('-msg', '--edit_message',
                        dest="Msg",
                        help="Modify the message that will send it,(please try without emoji)",
                        default="[Hi @Target_User, How are you?]",
                        required=False)
    parser.add_argument('-f', '--following',
                        dest="Following",
                        help="Do you want following users (True/False)",
                        default=False,
                        required=False)
    parser.add_argument('-save', '--save',
                        dest="Save",
                        help="Do you want save your users (True/False)",
                        default=True,
                        required=False)
    parser.add_argument('-img', '--pictures',
                        dest="Pictures",
                        help="Do you want block pictures (True/False)",
                        default=False,
                        required=False)
    return parser.parse_args()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(r"--user-data-dir=C:\Users\MON PC\AppData\Local\Google\Chrome\User Data\Default") # Path to your chrome profile or you can open chrome and type: "chrome://version/" on URL
chrome_driver_exe_path = abspath("C:\Python310\chromedriver.exe") # download from https://chromedriver.chromium.org/downloads
assert path.exists(chrome_driver_exe_path), 'chromedriver.exe not found!'

if parse_args().Pictures:
   #block imges.. to be fast
   prefs = {"profile.managed_default_content_settings.images": 2}
   chrome_options.add_experimental_option("prefs", prefs)

web = webdriver.Chrome(executable_path=chrome_driver_exe_path, options=chrome_options)
web.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


link_posts = []#links/liked_by
allUsers = []#this for saving in file
warning = ""
#extract posts from hashtag

def scroll():
    for i in range(1, int(parse_args().Scroll)):
     web.execute_script("window.scrollTo(0, window.scrollY + 5000)")
     sleep(1)

def main():
   if parse_args().Username != "" and parse_args().Password != "":
      web.get('https://www.instagram.com/')
      sleep(5)
      try: 
       web.find_element_by_name('username').send_keys(parse_args().Username)
       web.find_element_by_name('password').send_keys(parse_args().Password)
       web.find_element_by_xpath('//html//body//div[1]//section//main//div//article//div//div[1]//div//form//div//div[3]//button//div').click()
       sleep(5)
       start()
      except:
        print("\n-Error [authenticate]: Username or Password.\n")
      pass
      sleep(3)
   else: 
      start()

def start():
 for tag in parse_args().Hashtags:
    web.get('https://www.instagram.com/explore/tags/'+tag+'/')
    web.set_window_position(0, 0)
    web.set_window_size(700, 700)
    sleep(6)
    #extract urlPost from href attribute
    all_links = web.find_elements(By.CSS_SELECTOR, "a")
    for link in all_links:
        url = link.get_attribute('href')
        x = re.search("/p/", url)
        if x:
           link_posts.append(url+"liked_by/")

 link_posts = list(set(link_posts))#remove duplicated link
 sleep(3)
 #extract urlUser from href attribute
 users = []# users liked post for send message
 followed = 0
 for link in link_posts: 
    web.get(link)
    sleep(3)
    #scrolling to get more users
    scroll()
    #you can add your 
    if parse_args().Following:
        new = -1
        btns = web.find_elements(By.CSS_SELECTOR, "button ._aacl")
        for btn in btns:
            new += 1
            if re.search("You can not following more.", warning):
               break
            try:
               if btn.text =="Follow" or btn.text == "Suive" :
                 web.find_elements(By.CSS_SELECTOR, "button ._aacl")[new].click()
                 followed += 1
                 sleep(1)
            except:
                warning += "\n-You can not following more."
            pass
    newuserliked = []
    #extract users liked post
    all_users_links = web.find_elements(By.CSS_SELECTOR, "._ab8w a")
    for d in all_users_links:
        new_user = d.get_attribute('href')
        if len(new_user) > 26 and new_user not in users:
           users.append(new_user[26:len(new_user)-1])#cut username for send msg
           newuserliked.append(new_user[26:len(new_user)-1])  # cut username and add in arry for save in json
    newuserliked = list(set(newuserliked))#move duplicate user
    d = dict()
    d[link] = [d for d in newuserliked]
    allUsers.append(d)
 users = list(set(users))#final users list

 #send messages
 msgSend = 0
 if parse_args().Send:
   web.get('https://www.instagram.com/direct/new/')
   sleep(6)

   for i in users: #chage to users
    if re.search("You can not send more messages.", warning):
       break
    try:
     if parse_args().Msg == "[Hi @Target_User, How are you?]":
        message = "Hi @" + i+", How are you?"
     web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input').send_keys(i)
     sleep(3)
     # click on the username
     web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]/button').click()
     sleep(2)
     # next button
     web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
     sleep(5)
     # click on message area
     send = web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
     send.click()
     # types message
     sleep(2)
     send.send_keys(message)
     sleep(1)
     # send message
     send.send_keys(Keys.ENTER)
     sleep(2)
     msgSend += 1
     # clicks on direct option or pencl icon
     web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()
     sleep(2)
    except:
        warning += "\n-You can not send more messages."
        pass


 if parse_args().Sve:
   with open('allUsers.json', 'w') as f:
        json.dump(allUsers, f)
        f.close()
        warning += "\n-Save users successfully."

 col_names = ["TOTAL_POSTS", "TOTAL_USERS", "TOTAL_Message", "TOTAL_Followed","Warning"]
 datatable = [[len(link_posts), len(users), msgSend, followed, warning]]
 print(tabulate(datatable, headers=col_names, tablefmt="grid"))

main()
