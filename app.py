import os
import sys
import json

import requests
from flask import Flask, request
from weather import Weather

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "<h1> Hello world </h1>", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    except:
                        message_text = "BAD VALUE"

                    try:
                        message_text = message_text.encode('utf-8')
                    except UnicodeError:
                        print "string is not UTF-8"
                        message_text = "NON UNICODE"

                    handle_message(sender_id, message_text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def handle_message(sender_id, message_text):
    log("Type of message_text " )
    log(type (message_text))
    log("message as text")
    fileencoding = "utf-8"
    message_as_string = str(message_text)
    if("picture" in message_as_string):
        send_image(sender_id)
        return;
    if ("weather" in message_as_string):
        #weather_text = "In which city?"
        w = Weather("Boston,us")
        temp = w.temp
        weather_text = "The temperature is" + temp
        send_message(sender_id, weather_text)
        return;
    # we can add parsing and logic and task here
    send_message(sender_id, message_text + ' daddy <3')

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_image (recipient_id , url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQwY9Xlth-JC3201W5rdvRK0d0CDfYz9pNllk3SBW-_P7TkTP5d"):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload":{
                    "url": url
                    }
                }
            }
        # "message": {
            # "text": message_text
        # }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
