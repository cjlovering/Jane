from messages import *
from random import randint

def flip_coin (recipient_id):
    flip = randint (0,2) 

    result = "HEADS"

    if( flip is 0 ):
        result = "TAILS"

    send_message(recipient_id, result)


