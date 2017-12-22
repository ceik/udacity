from twilio.rest import Client
import twilio_auth

# Your Account SID from twilio.com/console
account_sid = twilio_auth.sid
# Your Auth Token from twilio.com/console
auth_token  = twilio_auth.token

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+6588888888", 
    from_="+15017250604",
    body="Hello from Python!")

print(message.sid)
