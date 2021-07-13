import requests
import time
import lxml
import win10toast
from bs4 import BeautifulSoup
import emailclient
import logging
from fake_headers import Headers

logging.basicConfig(filename=r'C:\users\vamsi\desktop\logs\stockchecker3060ti.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
toaster = win10toast.ToastNotifier()

URL = "https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html"

return_status = "nope"

to = "masked@gmail.com"
sender = "masked@gmail.com"
subject = "RPTech RTX 3060ti Stock Available!!!"
message_text_html  = r'Hi<br/>RTX 3060ti is available <b> <br/> https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html</b>'
#message_text_plain = "Hi\nPlain Email"
#attached_file = r'C:\Users\Me\Desktop\audio.m4a'

while return_status == "nope":
    try:
        content = requests.get(URL, headers=Headers().generate())
    except requests.ConnectionError as e:        
        logging.debug(e)

    soup = BeautifulSoup(content.text, "lxml")

    #findAll returns a list of div tags that have class 'pull-left retail'
    #And out of those tags the second tag has " Available Quantity : 0" string
    #Hence the use of [1] because list starts with 0 and 1 and so on
    k = soup.findAll('div', attrs={'class':'pull-left retail'})[1]
    #print(k)
    if  " Available Quantity : 0" in k:
        logging.debug("not available - " + str(k))
    elif " Available Quantity : 0" not in k:
        logging.debug("available!!!!")
        toaster.show_toast('Python', 'Stock Available!')
        #send email
        message_text_html = message_text_html + '<br/>' + str(k)
        emailclient.create_message_and_send(sender, to, subject, message_text_html)
        logging.debug("Mail Sent!")
        return_status="Available"
        break
    time.sleep(300)

logging.debug('----------End of Program----------')
#----------End of Main Block------------
