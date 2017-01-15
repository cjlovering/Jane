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
        choice = stories[random.randint(0, len(stories))]
        
        for segment in choice:        
            send_message(sender_id, segment)
            msg_wait(sender_id)
            time.wait(3)
            mode = get_most_common_word(segment)
            log(mode)
            send_image(sender_id, mode)


def get_most_common_word(stream):
    words = stream.split()
    counts = {}
    for w in words:
        if len(w) > 3:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1
    
    word, count = "", -1
    for key, value in counts.iteritems():
        if value > count:
            word, count = key, value
            

    return word

            
            
