import os
import sys
import json
import requests
import time

from random import randint
from flask import Flask, request
from image_search import *



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


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
        "sender_action":"typing_on"
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
