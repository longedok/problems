#encoding:utf-8

def tokenize(input):
    parsed = []
    token = u''
    for ch in input:
        if ch in [u'|', u'{', u'}']:
            if len(token) > 0:
                parsed.append(token)
                token = u''
            parsed.append(ch)
        else:
            token += ch
    if len(token) > 0:
        parsed.append(token)
    return parsed

def parse(tokens, parsed):
    i = 0
    temp = []
    while True:
        token = tokens[i]
        if token == '{':
            alts = []
            temp.append({u'alts': alts})
            tokens = parse(tokens[i+1:], alts)
            if len(alts) == 0:
                temp = temp[:-1]
            i = -1
        elif token == '}':
            if len(temp) <= 1:
                parsed += temp
            else:
                parsed.append(temp)
            return tokens[i+1:]
        elif token == '|':
            if len(temp) <= 1:
                parsed += temp
            else:
                parsed.append(temp)
            temp = []
        else:
            temp.append(token)
        i += 1
        if i == len(tokens):
            break
    parsed += temp

def output(parsed, string=''):
    if len(parsed) > 0:
        token = parsed[0]
        if type(token) == dict:
            for alt in token['alts']:
                if type(alt) == dict:
                    output([alt] + parsed[1:], string)
                elif type(alt) == list:
                    output(alt + parsed[1:], string)
                else:
                    output(parsed[1:], string+alt)
        else:
            output(parsed[1:], string+token)
    else:
        print string

if __name__ == '__main__':
    a = u"{Пожалуйста|Просто} сделайте так, чтобы это {удивительное|крутое|простое} тестовое предложение {изменялось {быстро|мгновенно} случайным образом|менялось каждый раз}."
    #a = u"{Please|Just} made this {wonderful|cool|simple} test sentence {changing {fast|instantly} randomly|changing every time}."
    import pprint
    class MyPrettyPrinter(pprint.PrettyPrinter):
        def format(self, object, context, maxlevels, level):
            if isinstance(object, unicode):
                return ("'%s'" % object, True, False)
            return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

    tokens = tokenize(a)
    parsed = []
    parse(tokens, parsed)
    pp = MyPrettyPrinter()
    pp.pprint(parsed)
    output(parsed)
