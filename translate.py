from yandex_translate import YandexTranslate

def handle_transl(message_in, target):
    #r = requests.get(https://translate.yandex.net/api/v1.5/tr.json/translate?key=<trnsl.1.1.20170115TO20150Z.5a7ee6b315a11aa3.083f6b10747c2f39183936fc5ec47ebccff59370
    translate = YandexTranslate('trnsl.1.1.20170115T035945Z.52ce8147859bea7e.b77e0f289f7e269c5714bd7f57d7d33b4f40705c') 
    tstring = (translate.translate(message_in, target))['text']
    print tstring[0].encode('utf-8')
    return tstring

handle_transl('cat', 'es')
