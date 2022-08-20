"""
Сюда лучше не лезть, эта х***я не объясняется.

Получаем код из таблицы юникода для каждого символа.
Каждый код переводим в 36-ричную СС (коды русских символов
из трёхзначных превращаются в двухзначные).
Каждую цифру новом коде меняем на символ.
"""


d = list('╸╷┯╴┻┨├╵╾┵┢┫┥┬┧╿╻╶┳╽┰┲┱╺┣┤┹┝┮┺┴╼╹┸┦┭')
number_system = '0123456789abcdefghijklmnopqrstuvwxyz'
splitter = '┪'
# d = '✢✣✤✥✦✧✩✪✫✬✭✮✯✰✱✲✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❅❆❇❈❉❊'
# splitter = '✠'


def encrypt(text_to_encrypt: str) -> str:
    """ Encrypts text """
    code = [ord(i) for i in text_to_encrypt]
    result = []

    for number in code:
        tmp = []
        while number > 0:
            tmp = [number % 36] + tmp
            number //= 36
        tmp_1 = ''
        for i in tmp:
            tmp_1+= d[i]
        result += [tmp_1]

    return splitter.join(result)


def decrypt(encr_message: str) -> str:
    """ Decrypts text """
    array = encr_message.split(splitter)
    result = ''
    mid_result = []

    for symbols in array:
        tmp = ''
        for symbol in symbols:
            index = d.index(symbol)
            tmp += str(number_system[index])

        mid_result += [int(tmp, 36)]
    
    for code in mid_result:
        result += chr(code)  

    return result


if __name__ == '__main__':
    print(a := encrypt('''Анекдот № 119:

— Для чего женщине нужен пупок?
— Для того, чтобы мужчина по пути вниз мог оставить там свою жвачку.'''))
    print(decrypt(a))