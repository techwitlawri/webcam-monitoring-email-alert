import smtplib
#import imghdr
from PIL import Image
from io import BytesIO
from email.message import EmailMessage

PASSWORD = "tkzg ddsx dvjk pmmu"
SENDER ="practicecode09@gmail.com"
RECEIVER = "practicecode09@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up"
    email_message.set_content("Hey, we just saw a new customer")

    with open(image_path, "rb") as file:
        content = file.read()
        image_data = BytesIO(content)
        img = Image.open(image_data)


        image_format = img.format
        print("Image format:", image_format)
    email_message.add_attachment(content, maintype="image", subtype=image_format)
    #email_message.add_attachment(content, maintype = "image", subtype= imghdr.what(None, content))

    gmail = smtplib.SMTP( "smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == '__main__':
    send_email(image_path = "images/58.PNG")

