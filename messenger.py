# use 'pip install twilio' to install twilio on your device.
import twilio
import twilio.rest
from twilio.rest import Client


class Messenger:
    client = None

    def __init__(self, account_sid, auth_token):
        # instantiating the Client
        self.client = Client(account_sid, auth_token)

    # sending message
    # from number is provided by twilio
    # to number has to be verified number on twilio
    def send(self, content, from_number, to_number):
        message = self.client.messages.create(body=content, from_=from_number, to=to_number)
        # printing the sid after success
        print(message.sid)


# # Driver code
# messenger = Messenger('AC529796f7c206f315a9c2afdaba05adb1', 'b808d59fbd7682f42ab6c951a51349c4')
# messenger.send('Dear Sir/Madam. You have been in close contact with someone who has COVID-19. Self isolate for 14 days and get yourself tested in the following locations near you at www.onemap.gov.sg/main/v2/pcrtmap/',
#                '+14439988401', '+6583820323')
