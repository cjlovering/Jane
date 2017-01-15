from messages import *
from random import randint
from constants import *

def flip_coin (recipient_id):
    flipping_image = "https://lh3.googleusercontent.com/2AIIu2_mmmWUL8LBUOJhyUE_VFr7-Ca1FEGJNDTRbCLL3IFtHi4ZpanRzR3RiIpMJ4Nj=w300"
    head_image_url = "https://tse1.mm.bing.net/th?&id=OIP.Md28c8747e6c37360feaa4bd29355545do0&w=298&h=300&c=0&pid=1.9&rs=0&p=0&r=0"
    flipping_image = "https://lh3.googleusercontent.com/2AIIu2_mmmWUL8LBUOJhyUE_VFr7-Ca1FEGJNDTRbCLL3IFtHi4ZpanRzR3RiIpMJ4Nj=w300"

    send_image(recipient_id, flipping_image )
    tail_image_url = "https://tse4.mm.bing.net/th?id=OIP.Ma2303d204768c9b90efbb9ba38aa67a1o0&pid=15.1" 
    flip = randint (0,2) 

    result = "HEADS"

    if( flip is 0 ):
        result = "TAILS"
        send_message(recipient_id, "TAILS") 
        send_image(recipient_id , tail_image_url)
    else :
        send_message(recipient_id, "HEADS")
        send_image(recipient_id, head_image_url)

    return result
    


# returns state and message_out 
def handle_coin_flip(recipient_id ,  message_in):
    msg_wait(recipient_id)
    if(COINFLIP in message_in):
        return COINFLIP , "Pick Heads or Tails"
    else:
        choice = None
        if("heads" in message_in):
            choice = "HEADS"
        elif("tails" in message_in):
            choice = "TAILS"

        if(choice is None):
            return COINFLIP , "Invalid option, pick Heads or Tails"
        else:
            result = flip_coin(recipient_id)
            if(result == choice):
                return None , "You Win! Luckerdog"
            else :
                return None, "Loser! Low effort.."



