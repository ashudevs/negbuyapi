from email import message
import smtplib, ssl
import os

def contact_function(message):
    port = 25  # For SSL
    password = os.environ['user_cred']

    # Create a secure SSL context
    context = ssl.create_default_context()

    sender_email = "amirmohd233@gmail.com"
    receiver_email = "contactus@negbuy.com"
    with smtplib.SMTP_SSL("relay-hosting.secureserver.net", port, context=context) as server:
        server.login("amirmohd233@gmail.com", password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)
        return True

#bxwwkekhiutnlwhd