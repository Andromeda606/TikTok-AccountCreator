from selenium import webdriver
import time
import json
import random

#Import Kısmı

#Json Dosyasından Veri Aktarılıyor
data = open("settings.json", "r+", encoding="utf8")
jsondata = json.load(data)
data.close()

emailEnd = jsondata["eMailEnd"] #eMail sonu çekiliyor
passw = jsondata["password"] #Şifre Çekiliyor
email = jsondata["email"] #eMail çekiliyor
emailFull = email + "+" + str(random.randint(1, 99999)) + "@" + emailEnd #eMail toplanıyor
browser = webdriver.Firefox(executable_path=jsondata["geckoPath"]) #Gecko konumu alınıyor
browser.implicitly_wait(10) #10 sn içinde istediğimiz ortaya çıkmaz ise hata ver

#Fonksiyonların bulunduğu yer
def gMailVeriAktar():
    import gmailReader as gr  # mail readeri ediniyoruz
    code = gr.getmail() #maili çekiyoruz
    codePath = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[5]/div/input') #kod konumu
    if not(codePath.get_property("value") == code): #Eğer kod aynı değil ise ekrana yazsın
        try:
            codePath.clear()
        except:
            print("Silme işlemi gerçekleştirilemedi")
        codePath.send_keys(code)
        kayitOlBas()
    else: #Aynı ise bunu tekrar açsın
        if browser.current_url is None:
            exit()
        else:
            gMailVeriAktar()


def kayitOlBas():
    global emailFull,passw
    try:
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/button').click()
        time.sleep(1) #Sonucu bekleyelim
        sonuc = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/form/div[4]/div[6]/div')
        if sonuc.get_attribute("innerHTML")== "Incorrect code":
            #Kod yanlış ise TikToku dinleyip tekrar kod istiyoruz
            time.sleep(1)
            gMailVeriAktar()
        elif sonuc.get_attribute("innerHTML") == "Verification failed. Please click Resend and try again.":
            print("Kodu girmediniz, Birdaha deneniyor")
            time.sleep(1)
            kayitOlBas()
        else:
            try:
                skipPath = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/button[2]")
                print("hesap oluştu, mailler siliniyor ve yeni hesaba geçiliyor")
                skipPath.click() #Skipe basılıyor
                #basarilikayit(emailFull, passw) #Dosyaya yazılıyor
                import gmailReader as gr #Mailleri siliyoruz
                gr.deletemail() #Mailleri silmeyi emrettik
                browser.quit() #İşimiz burda bitiyor
            except:
                print("hesap açılmadı")

        #TODO ELSE BURADA OLACAK VE BURDA KAYIT OLMA TAMAMLANDIĞINDA OLACAKLAR OLACAK!
    except:
        try:
            print(browser.current_url)
        except:
            import bot
            exit()
        #Eğer ekrana browser ismi yazılmıyor ise çıksın, Program işi bittiği halde açık kalmasın
        try:
            skipPath = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/button[2]")
            print("hesap oluştu, mailler siliniyor ve yeni hesaba geçiliyor")
            skipPath.click()  # Skipe basılıyor
            basarilikayit(emailFull, passw) #Dosyaya yazılıyor
            import gmailReader as gr  # Mailleri siliyoruz
            gr.deletemail()  # Mailleri silmeyi emrettik
            browser.quit()  # İşimiz burda bitiyor
            import os,sys
            os.startfile(__file__)
            sys.exit()
        except:
            if(browser.current_url=="https://www.tiktok.com/login/download-app"):
                print("HESAP YARI DOGA DÜŞTÜ")
                basarilikayit(emailFull, passw)  # Dosyaya yazılıyor
                import gmailReader as gr  # Mailleri siliyoruz
                gr.deletemail()  # Mailleri silmeyi emrettik
                browser.quit()  # İşimiz burda bitiyor
                import os, sys
                os.startfile(__file__)
                sys.exit()
            print("")
            print("Kodu girmediniz, Birdaha deneniyor")
            time.sleep(1)
            kayitOlBas()

def basarilikayit(email, password):
    veri = open("users.txt","a")
    veri.write(email+":"+password+"\n")
#Fonksiyonlar bitti

#VERİLER AKTARILDI, PROGRAM BAŞLIYOR

browser.get("https://www.tiktok.com/signup/phone-or-email/email?lang=en") #Kayıt olma kısmına giriyor
emailPath = browser.find_element_by_name("email")
passPath = browser.find_element_by_name("password")
#eMail ve Pass konumu alınıyor
emailPath.send_keys(emailFull)
passPath.send_keys(passw)
browser.get('javascript:document.getElementsByClassName("select-container-1DrEI")[0].click();document.getElementsByClassName("list-item-2xmNY")[0].click();document.getElementsByClassName("select-container-1DrEI")[1].click();document.getElementsByClassName("list-item-2xmNY")[1].click();document.getElementsByClassName("select-container-1DrEI")[2].click();document.getElementsByClassName("list-item-2xmNY")[40].click();document.getElementsByClassName("login-button-86o6Z")[0].click();')
gMailVeriAktar()
#Veriler yazılıyor

