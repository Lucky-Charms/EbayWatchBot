from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from threading import Thread
import random
import string
import os
import time

def createSession():
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    driver = webdriver.Chrome()
    return driver

def login(username, password, driver):
    driver.get("https://www.ebay.com/signin")
    time.sleep(1)
    driver.find_element_by_id("userid").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("sgnBt").click()
    redirectedUrl = str(driver.current_url)
    #Code to check for the suspension notice or if entered wrong password. 
    if ('https://www.ebay.com/signin' in redirectedUrl):
        print("[ERROR] Login Issue")
        return False
    return True

def addToWatchList(productURL,driver):
    time.sleep(0.5)
    driver.get(productURL)
    time.sleep(1)
    watchingElement = driver.find_element_by_class_name("vi-atw-txt")
    if ('watching' in watchingElement.text.lower()):
        print('[ERROR] Already Watched. ')
        driver.close()
    else:
        driver.find_element_by_id("vi-atl-lnk").click()
        print('[SUCCESS] Successfully Watched! ')
        time.sleep(1)
        driver.quit()

def parseTXT():
    os.chdir("C:\\####\\#####\\#####\\####\\####") #Change this to the directory where your accounts.txt is located at.
    with open("Accounts.txt") as accountsList:
        accounts = accountsList.read().splitlines()
        return accounts

#Method to generate ebay accounts and append it into Accounts.txt
#Limits to 4 accounts per day.
def generateAccount(numAccount):
    password = "washedj1" #Set this to whatever password you want
    registerLink = "https://reg.ebay.com/reg/PartialReg?ru=https%3A%2F%2Fwww.ebay.com%2F"
    for i in range(numAccount):
        firstName = randomName()
        lastName = randomName()
        email = randomCatchall('floppedcart.club')
        driver = webdriver.Chrome()
        driver.get(registerLink)
        driver.find_element_by_name("firstname").send_keys(firstName)
        driver.find_element_by_name("lastname").send_keys(lastName)
        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_name("PASSWORD").send_keys(password)
        time.sleep(1)
        driver.find_element_by_id("ppaFormSbtBtn").click()
        print("[SUCCESS] Account Created!")
        print("Login: " + email)
        print("Password: " + password)
        time.sleep(5)
        updateAccountsTXT(email, password)

#Method to generate random catchalls
def randomCatchall(domain):
    randomLength = int(random.choice(string.digits)) + 1
    Randomid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(randomLength))
    catchall = Randomid + "@"+ domain
    return catchall

#Method to generate random names
def randomName():
    randomLength = int(random.choice(string.digits)) + 4
    name = ''.join(random.choice(string.ascii_letters) for _ in range(randomLength))
    return name

def updateAccountsTXT(user, passw):
    os.chdir("C:\\####\\####\\#####\\Python\\EbayBot") #Change this to the directory with your accounts.txt
    f = open("Accounts.txt", "a")
    text = user + ":" + passw + "\n"
    f.write(text)

def task(ebayLink):
    list_of_accounts = parseTXT()
    taskDone=False
    for account in list_of_accounts:
        account_split = account.split(":")
        user = account_split[0]
        passw = account_split[1]
        sess = createSession()
        successLogin=login(user, passw, sess)
        if(successLogin == True):            
            addToWatchList(ebayLink, sess)
    print("Finished Watching.")

def startWatch(prodLink):
        taskDone = False
        list_of_accounts = parseTXT()

#Main
link = "https://www.ebay.com/itm/123488648701"
task(link)