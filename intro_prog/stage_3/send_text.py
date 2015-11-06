# Lesson 3.3: Use Classes
# Mini-Project: Send Text

# It can be important for businesses to automate sending
# text messages. In this mini-project we'll uses classes
# to send a text message using Twilio, a library we'll
# download from the Internet and add to Python.

from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACddafbb1f856f8e5ecd7b1f9beb23688c"
# auth_token  = "{{ b4b7bcdfd6b79e40301c383a1af5bbb4 }}"
auth_token  = "b4b7bcdfd6b79e40301c383a1af5bbb4"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
    body="Hi, test message from send_text.py!",
    to="+6582673040",    # Replace with your phone number
    from_="+14807870313") # Replace with your Twilio number
print message.sid

# Your code here.
