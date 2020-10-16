from selenium import webdriver
import time
import json
import random

#Import

data = open("settings.json", "r+", encoding="utf8")
jsondata = json.load(data)
data.close()

emailEnd = jsondata["eMailEnd"]
passw = jsondata["password"]
email = jsondata["email"]
emailFull = email + "+" + str(random.randint(1, 99999)) + "@" + emailEnd
browser = webdriver.Firefox(executable_path=jsondata["geckoPath"])
browser.implicitly_wait(10)

#Functions
def getGmail():
    import gmailReader as gr
    code = gr.getmail()
    codePath = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[5]/div/input')
    if not(codePath.get_property("value") == code):
        try:
            codePath.clear()
        except:
            print("Deletion could not be performed")
        codePath.send_keys(code)
        Register()
    else:
        if browser.current_url is None:
            exit()
        else:
            getGmail()


def Register():
    global emailFull,passw
    try:
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/button').click()
        time.sleep(1)
        result = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[6]/div')
        if result.get_attribute("innerHTML")== "Incorrect code":
            time.sleep(1)
            getGmail()
        elif result.get_attribute("innerHTML") == "Verification failed. Please click Resend and try again.":
            print("Verification failed. Please click Resend and try again.")
            time.sleep(1)
            Register()
        else:
            try:
                skipPath = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/button[2]")
                print("The account has been created, the mails are deleted and the new account is transferred")
                skipPath.click()

                import gmailReader as gr
                gr.deletemail()
                browser.quit()
            except:
                print("no account opened")
    except:
        try:
            print(browser.current_url)
        except:
            import bot
            exit()
        try:
            skipPath = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/button[2]")
            print("The account has been created, the mails are deleted and the new account is transferred")
            skipPath.click()
            successReg(emailFull, passw)
            import gmailReader as gr
            gr.deletemail()
            browser.quit()
            import os,sys
            os.startfile(__file__)
            sys.exit()
        except:
            if(browser.current_url=="https://www.tiktok.com/login/download-app"):
                successReg(emailFull, passw)
                import gmailReader as gr
                gr.deletemail()
                browser.quit()
                import os, sys
                os.startfile(__file__)
                sys.exit()
            print("You did not enter the code, try again")
            time.sleep(1)
            Register()

def successReg(email, password):
    veri = open("users.txt","a")
    veri.write(email+":"+password+"\n")
#Functions end

browser.get("https://www.tiktok.com/signup/phone-or-email/email?lang=en")
emailPath = browser.find_element_by_name("email")
passPath = browser.find_element_by_name("password")

emailPath.send_keys(emailFull)
passPath.send_keys(passw)
browser.get('javascript:document.getElementsByClassName("select-container-36J-Y")[0].click();document.getElementsByClassName("list-item-26TR9")[0].click();document.getElementsByClassName("select-container-36J-Y")[1].click();document.getElementsByClassName("list-item-26TR9")[1].click();document.getElementsByClassName("select-container-36J-Y")[2].click();document.getElementsByClassName("list-item-26TR9")[40].click();document.getElementsByClassName("login-button-Rt4Hk")[0].click();')
getGmail()

