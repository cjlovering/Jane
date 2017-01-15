from messages import *
import random
from story_gen import story_gen, get_sequence



def handle_story(state, sender_id, message_in):
    # pattern, model, int_to_char, n_vocab, n_chars = story_gen()
    # log("Finished building model...")
    # build story
    potential = ["Let me think...", "I've got a good one...", "I made this one up myself...", "This happened a long time ago..."]
    send_message(sender_id, potential[random.randint(0,3)])
    msg_wait(sender_id)
    with open('stories.json') as data_file:
        stories = json.load(data_file)
        log("OPENED story file : {0}".format(history))
        
        choice = random.randint(0, len(stories))
        
        for segment in choice:        
            send_message(sender_id, message)
            msg_wait(sender_id)
            
            mode = get_most_common_word(segement)
            send_image(sender_id, mode)


def get_most_common_word(stream):
    words = stream.split()
    for w in words:
        if w != 'the' and w != 'a':
            return w
    

            
            
