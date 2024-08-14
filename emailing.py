import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "tkzg ddsx dvjk pmmu"
SENDER ="practicecode09@gamil.com"
RECEIVER = "practicecode09@gamil.com"


def send_email(image_path):
    email_message = EmailMessage
    email_message["subject"] = "New customer showed up"
    email_message.set_content("Hey, we just saw a new customer")

    with open(image_path, "rb") as file:
        content = file.read()
        email_message.add_attachment(content, maintype = "image", subtype= imghdr.what(None, content))

        gmail = smtplib.SMTP("smtp.gmail.com", 587)
        gmail.ethlo()
        gmail.starttls()
        gmail.login(SENDER, PASSWORD)
        gmail.sendmail(SENDER,RECEIVER, email_message)