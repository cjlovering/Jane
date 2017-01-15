from messages import *
import random
from story_gen import story_gen, get_sequence



def handle_story(state, sender_id, message_in):
    send_message(sender_id, "One second, looking through the libraries...")
    pattern, model, int_to_char, n_vocab, n_chars = story_gen()
    log("Finished building model...")
    # build story
    potential = ["Let me think...", "I've got a good one...", "I made this one up myself...", "This happened a long time ago..."]
    send_message(sender_id, potential[random.randint(0,3)])

    msg_wait(sender_id)
    for i in range(5):
        pattern , result = get_sequence(pattern, model, int_to_char, n_vocab, n_chars)
        message = "".join(result)
        send_message(sender_id, message)
        msg_wait(sender_id)

    # send story
    # format story
    # sequence story, add images...
