from messages import *
from random import random
from story_gen import story_gen

def handle_story(state, sender_id, message_in):
    # build story
    potential = ["Let me think...", "I've got a good one...", "I made this one up myself...", "This happened a long time ago..."]
    send_message(sender_id, potential[random.randint(0,3))
    story = story_gen(message_in)
    # send story
    # format story
    # sequence story, add images...
    send_message(sender_id, story)
