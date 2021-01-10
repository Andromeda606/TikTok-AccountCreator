from selenium import webdriver
import time
import json
import random

# Import

data = open("settings.json", "r+", encoding="utf8")
jsondata = json.load(data)
data.close()

emailEnd = jsondata["eMailEnd"]
passw = jsondata["password"]
email = jsondata["email"]
emailFull = email + "+" + str(random.randint(1, 99999)) + "@" + emailEnd
options = webdriver.FirefoxOptions()
#options.add_argument('-headless')
browser = webdriver.Firefox(executable_path=jsondata["geckoPath"],options=options)
#browser = webdriver.Chrome(executable_path=jsondata["chromePath"])
browser.implicitly_wait(10)


# Functions
def getGmail():
    import gmailReader as gr
    print("getMail")
    code = gr.getmail()
    codePath = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[5]/div/input')
    if not (codePath.get_property("value") == code):
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
    global emailFull, passw
    try:
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/button').click()
        time.sleep(1)
        result = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[6]/div')
        if result.get_attribute("innerHTML") == "Incorrect code":
            time.sleep(1)
            getGmail()
        elif result.get_attribute("innerHTML") == "Verification failed. Please click Resend and try again.":
            print("Verification failed. Please click Resend and try again.")
            time.sleep(1)
            Register()
        elif result.get_attribute("innerHTML") == "Verification failed. Please click Resend and try again.":
            print("YOUR IP BLOCKED!")
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
            import os, sys
            os.startfile(__file__)
            sys.exit()
        except:
            if (browser.current_url == "https://www.tiktok.com/login/download-app"):
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
    veri = open("users.txt", "a")
    veri.write(email + ":" + password + "\n")


# Functions end
cookies = "tt_webid=6884877451467179525; tt_webid_v2=6884877451467179525; s_v_web_id=verify_kgev18p4_wS31yIAd_DbQv_4d9Y_944R_3giruvGhbAwM; _ga=GA1.2.1495663218.1603010452; _gid=GA1.2.224102598.1603010452; passport_csrf_token=1686c19f83b8da0c0dbf1634f55f933c; odin_tt=e93bab047745d7a898fcdd155f575acb181bd17df20c8d98bc5963ad3292070aaf51b5e4388c883a8c17965c0dd5b852532e783b6b792ea69624dcff21466a6b; store-idc=maliva; store-country-code=tr; sid_guard=e41bbe2a5233598221d4d35fed7b67cb%7C1603011367%7C21600%7CSun%2C+18-Oct-2020+14%3A56%3A07+GMT; uid_tt=8492306fe5c1e3c2b593491b1a2b9c21; uid_tt_ss=8492306fe5c1e3c2b593491b1a2b9c21; sid_tt=e41bbe2a5233598221d4d35fed7b67cb; sessionid=e41bbe2a5233598221d4d35fed7b67cb; sessionid_ss=e41bbe2a5233598221d4d35fed7b67cb; MONITOR_WEB_ID=6884877451467179525".split(
    ";")


browser.get("https://www.tiktok.com/signup/phone-or-email/email")
emailPath = browser.find_element_by_name("email")
passPath = browser.find_element_by_name("password")
#for i in cookies:
#    cookie = i.split("=")
#    browser.add_cookie({"name": cookie[0], "value": cookie[1]})

emailPath.send_keys(emailFull)
passPath.send_keys(passw)
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[1]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[1]/ul/li[5]").click()
browser.find_element_by_xpath("/html/body/div[1]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[2]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[2]/ul/li[5]").click()
browser.find_element_by_xpath("/html/body/div[1]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[3]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[2]/div[3]/ul/li[29]").click() #age
browser.find_element_by_xpath("/html/body/div[1]/div").click()
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/div[4]/div[5]/button").click() #send code button
getGmail()
