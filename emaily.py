import smtplib
import ssl

class SendMail:
    def __init__(self, message):
        self.message = message
        ctx = ssl.create_default_context()
        password = "umltdjorwntkikil"    # Your app password goes here
        sender = "dsadiq620@gmail.com"    # Your e-mail address
        receiver = "danielsadiq93@gmail.com" # Recipient's address
        send_message = self.message.encode('utf-8')
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, send_message)