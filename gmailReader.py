import imaplib, email
import json
import re

data = open("settings.json", "r+", encoding="utf8")
lines = json.load(data)
email = lines["email"] + "@" + lines["eMailEnd"]
password = lines["gmailPass"]
regex = r"20px;color: rgb\(22,24,35\);font-weight: bold;\">(.*?)<\/p"

def getmail():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email, password)
    imap.select("INBOX")

# number of top emails to fetch
    tmp, data = imap.search(None, 'ALL')
    stra = ""
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        stra += str((num, data[0][1]))
    matches = re.finditer(regex, stra, re.MULTILINE)
    array = []
    for matchNum, match in enumerate(matches, start=1):
        array += [match.groups()[0]]
    imap.close()
    if len(array) == 0:
        return ""
    elif(len(array) == 1):
        return array[0]
    else:
        return array[len(array)-1]
def deletemail():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email, password)
    imap.select("INBOX")
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
        imap.store(num, '+FLAGS', '\\Deleted')
    imap.expunge()
    print("Deleted All Mails!")
print(getmail())
