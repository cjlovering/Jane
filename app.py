import os
import sys
import json
import requests
import time

import random
from random import randint
from flask import Flask, request

from weather import handle_weather
from story import handle_story
from image_search import *
from messages import *
from constants import *
from coin_flip import *
from chat import *

app = Flask(__name__)
history = None
session_length = 15000  # 2 1/2 min



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
    random.seed()
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        # TODO: just repond to last message
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                # Messageing_event is type dict
                if messaging_event.get("message"):  # someone sent us a message
                    # u'message', u'timestamp', u'sender', u'recipient'
                    log ("Values of Message_event : {0}".format(messaging_event.items()))
                    log ("\nValues as JSON : {0}".format(json.dumps (messaging_event , indent=2)))
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
    message_out = ""
    message_as_string = str(message_text)

    connected, new, state, user_info, messages = get_state(sender_id)

    if user_info is None:
        user_info = None #get_user_info(sender_id)


    if not connected:
        # if not connected, respond!
        if new:
            # send greeting message
            message_out = "Hey there, nice to meet you! :)"
            send_message(sender_id, message_out)
            if user_info is not None:
                message_out = "Cool name! {0}, i like it... ;)".format(user_info["first_name"])
                send_message(sender_id, message_out)
        else:
            # send welcome-back message
            if user_info is not None:
                message_out = "Great to see you again, {0}!".format(user_info["first_name"])
                send_message(sender_id, message_out)
            else:
                message_out = "Great to see you again!"
                send_message(sender_id, message_out)

    if STORY in message_as_string or state is not None and state == STORY:
        pass
    elif RPS in message_as_string or state is not None and state == RPS:
        state, message_out = handle_rps(state, sender_id, message_as_string)
    elif PICTURE in message_as_string or state is not None and state == STORY:
        msg_wait(sender_id)
        send_image(sender_id , getURL(message_as_string))
    elif WEATHER in message_as_string or state is not None and state == WEATHER:
        state, message_out,  description = handle_weather(state, message_as_string)
        send_message(sender_id, message_out)
        if description is not None:
            log("Description is not None, Sending image :  {0}".format(description))
            send_image(sender_id , getURL("weather " + description))
    elif COINFLIP in message_as_string or state is not None and state == COINFLIP :
        state , message_out  = handle_coin_flip(sender_id, message_as_string)
        send_message (sender_id, message_out)


    else:
        # generic reponse
        message_out = respond(message_text)
        send_message(sender_id, message_out)

    # store current information
    # update_state(sender_id, state, user_info, message_in, message_out)
    log("sender_id  {0} , state {1}".format(  sender_id , state))
    update_state(sender_id, state, user_info, message_as_string , message_out)





def get_state(sender_id):
    """
    returns connected, new, state, user_info, messages
    """
    global history
    if history is None:
        try:
            with open('STATE.json') as data_file:
                history = json.load(data_file)
                log("OPENED state file : {0}".format(history))
        except:
            history = {}

    if sender_id in history:
        current_time = time.time()
        time_stamp, state, user_info, messages = history[sender_id]

        if current_time - int(time_stamp) < session_length:
            # user is in a current session
            return True, False, state, user_info, messages
        else:
            # user has been in a session but is not currently
            return False, False, None, user_info, None

    # user is new
    return False, True, None, None, None

def update_state(sender_id, state, user_info, message_in, message_out):
    global history
    time_stamp = time.time()
    history[sender_id] = (time_stamp, state, user_info, (message_in, message_out))
    with open('STATE.json', 'w') as outfile:
            json.dump(history , outfile)
            log("WRITE state file : {0}".format(history))

def get_user_info(target_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"],
        "fields": "first_name,last_name,profile_pic,locale,timezone,gender"
    }
    url = "https://graph.facebook.com/v2.6/<{0}>".format(target_id)
    r = requests.get(url, params=params)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return {}
    else:
        data = None
        try:
            data = r.json()
        except:
            data = {}
        return data

def handle_rps(state, sender_id, message_in):
    if state is None:
        message_out = "Let's play! Prepare yourself."
        send_message(sender_id, message_out)
        return (('!rps'), message_out)

    else:
        message_out = play_rps(message_in)
        send_message(sender_id, message_out)
        return (None, None)

def play_rps(userThrow):
    val = randint(0,2)
    if("rock" in userThrow):
        userVal = 0
        #userThrow = "rock"
    elif("paper" in userThrow):
        userVal = 1
        #userThrow = "paper"
    elif("scissors" in userThrow):
        userVal = 2
        #userThrow = "scissors"
    else:
        return "Not a valid option. Jane wins by default!"
    if val == 0:
        if userVal == 0:
            return "Jane meets your unstoppable rock with an immovable rock."
        elif userVal == 1:
            return "Jane also throws paper.  What are the chances."
        else:
            return "You and Jane are equally matched in the art of the blade."
    elif val == 1:
        if userVal == 1:
            return "You place a napkin on Jane's boulder.  You feel a sense of accomplishment."
        elif userVal == 2:
            return "You assail Jane's paper wih a pair of wicked blades.  How contemptible."
        else:
            return "Jane's scissors break upon your rocks."
    else:
        if userVal == 0:
            return "Jane envelops your rock within her fibrous embrace."
        elif userVal == 1:
            return "Jane eviscerates your paper and your dreams."
        else:
            return "Jane wins.  Was there ever any doubt?"


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    import nltk
    nltk.download()
    history = None
    app.run(debug=True)
