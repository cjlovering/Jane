from yandex_translate import YandexTranslate

dict = {'english': 'en', 'spanish': 'es', 'italian': 'it', 'greek': 'el', 'russian': 'ru', 'swedish':'sv', 'dutch':'nl'}

def handle_transl(message_in):
    phrase = []
    words = ""
    phrase = message_in.split(" in ")
<<<<<<< HEAD
    words = None
    if "translate" in phrase:
=======
    if "translate" in phrase[0]:
>>>>>>> 5d5bdcf8fe9d90899c09db1e229721e61d5ba568
        # delete
        words = phrase[0].replace("translate","")
    target = dict[phrase[1]]
    translate = YandexTranslate('trnsl.1.1.20170115T035945Z.52ce8147859bea7e.b77e0f289f7e269c5714bd7f57d7d33b4f40705c')
    tstring = (translate.translate(words, target))['text']
    print tstring[0].encode('utf-8')
    return tstring[0].encode('utf-8')

handle_transl("translate cat in spanish")
