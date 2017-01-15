# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient
import re

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACe2e697548218754dc7d33f509f5e6979"
auth_token  = "3d2791e68e8fd611e09d598ffa1736b9"
client = TwilioRestClient(account_sid, auth_token)

def handle_call(state, message_in):
    r = re.compile(r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')
    results = r.findall(message_in)
    if results:
        stripped = re.sub('[!@#$-)(]', '', "".join(results[0]))
        number= '+1' + stripped
        call = client.calls.create(url="http://demo.twilio.com/docs/voice.xml",
            to=number,
            from_="+14013563073")

    if not call:
        message_out = "Sorry I cannot reach you :/"
        state = None
    else:
        state = "state"
        message_out = "Calling..."

    return (state), message_out
