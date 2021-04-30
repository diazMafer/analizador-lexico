from tree import generate_tree
from direct import directo
from utils import word_break

#documentacion from page 6 of pdf https://ssw.jku.at/Research/Projects/Coco/Doc/UserManual.pdf 
RESERVERD_KEYWORDS = ["ANY", "CHARACTERS", "COMMENTS", "COMPILER", "CONTEXT",
"END", "FROM", "IF", "IGNORE", "IGNORECASE", "NESTED", "out", "PRAGMAS",
"PRODUCTIONS", "SYNC", "TO", "TOKENS", "WEAK"]
OPERATORS = ['Γ', 'Ꮬ'] #or y concatenacion nueva definicion para no entorpecer con el . de characters, tokens o mas


def analized_chars(characters):
    character_parsed = {}
    for c in characters:
        temp_string = ""
        flag = False
        i = 0
        chars_regex = ""            
        while i < len(characters[c]):
            if characters[c][i] == '"' or characters[c][i] == "'":
                flag = not flag
                if not flag:
                    temp_string = temp_string[:-1] + "Ꮽ"
                    chars_regex += temp_string 
                    temp_string = ""
                else:
                    temp_string += "Ꮼ" #abro parentesis
            elif flag:
                temp_string += characters[c][i] + "Γ"
            elif characters[c][i] == "+":
                chars_regex += "Γ"
            elif temp_string + characters[c][i] in character_parsed:
                chars_regex += character_parsed[temp_string+characters[c][i]]
                temp_string = ""
            elif temp_string == ".":
                if characters[c][i] == ".":
                    start = chars_regex[-2]
                    finish = ""
                    while i < len(characters[c]):
                        if characters[c][i] == "'":
                            break
                        i += 1
                    finish = characters[c][i + 1]
                    j = ord(start)
                    while j < ord(finish):
                        chars_regex += "Γ" + chr(j)
                        j += 1
                    chars_regex += "Γ" + finish
            elif temp_string == "CHR(":
                number = ""
                while i < len(characters[c]):
                    if characters[c][i] == ")":
                        break
                    elif characters[c][i] == " ":
                        pass
                    else:
                        number += characters[c][i]
                    i += 1
                number = int(number)
                symbol = chr(number)
                chars_regex += symbol
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parsed[c] = "Ꮼ" +  chars_regex + "Ꮽ"
        if c == "stringletter":
            finish = 128
            start = 0
            chars_regex == ""
            while start < finish:
                if start == 13 or start == 10 or start == 9 or start == 34:
                    pass
                else:
                    chars_regex +=  chr(start) + "Γ" 
                start += 1
            chars_regex += chr(finish)
            character_parsed[c] = "Ꮼ" +  chars_regex + "Ꮽ"
        elif c == "MyANY":
            finish = 128
            start = 0
            chars_regex == ""
            while start < finish:
                if start == 43 or start == 45 or start == 46 or start == 40 or start == 41 or start == 61 or start == 91 or start == 92 or start == 123 or start == 125 or start == 124 or start == 60 or start == 62 :
                    pass
                else:
                    if chr(start) == " ":
                        chars_regex +=  repr(chr(start)) + "Γ" 
                    else:
                        chars_regex +=  chr(start) + "Γ" 
                start += 1
            chars_regex += chr(finish)
            character_parsed[c] = "Ꮼ" +  chars_regex + "Ꮽ"
        elif c == "operadores":
            p =[43,45,46,40,41,61,91,92,123,125,124,60,62]
            for i in p[:-1]:
                chars_regex +=  chr(i) + "Γ"
            chars_regex += chr(p[-1])
            character_parsed[c] = "Ꮼ" +  chars_regex + "Ꮽ"

    return character_parsed

def analyzed_keywords(keywords,character_parsed):
    keywords_parsed = {}
    for k in keywords:
        word = keywords[k][:-1]
        i = 0
        temp = ""
        flag = False
        while i < len(word):
            if word[i] == '"':
                flag = not flag
                if not flag:
                    temp = temp[:-1] +  "Ꮽ" #cerramos parentesis
                else:
                    temp += "Ꮼ"
            else:
                temp += word[i] + "Ꮬ"
            i += 1
        keywords_parsed[k] = temp
    return keywords_parsed

def analyzed_tokens(tokens, characters):
    tokens_parse_lines = {}
    for t in tokens:
        token = tokens[t]
        i = 0
        temp = ""
        individual_regex = ""
        flag = False
        while i < len(token):
            temp += token[i]
            if temp in characters:
                og = temp
                temp = word_break(token, characters, i, temp)
                if og != temp:
                    i += len(temp) - len(og)
                if flag:
                    individual_regex += characters[temp] + "ᏭΦ"
                else:
                    individual_regex += characters[temp]
                temp = ""
            if temp == "|":
                individual_regex = individual_regex[:-2] + "Γ"
                temp = ""
            if temp == "{":
                flag = not flag
                individual_regex += "ᏜᏬ"
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            if temp == "[":
                second_flag = True
                if individual_regex != "":
                    individual_regex += "Ꮬ"
                individual_regex += "Ꮼ"
                temp = ""
            if temp == "]":
                second_flag = False
                individual_regex += " ΠᏭᏜ"
                temp = ""
            if temp == "(":
                individual_regex += "Ꮼ"
                temp = ""
            if temp == ")":
                individual_regex += "Ꮽ"
                temp = ""
            if temp == '"':
                inner = ""
                i += 1
                while i < len(token):
                    if token[i] == '"':
                        break
                    inner += token[i]
                    i += 1
                if individual_regex != "" :
                    individual_regex += "ᏜᏬ" + inner + "Ꮽ"
                else:
                    individual_regex += "Ꮼ" + inner + "Ꮽ"
                if token[i + 1] != "" and token[i + 1] != "\n" and token[i + 1] != ".":
                    individual_regex += "Ꮬ"
                temp = ""
            if temp == "CHR(":
                number = ""
                if tokens[t][i+3] == "." and i+4 <= len(tokens[t]):
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            number += tokens[t][i]
                        i += 1
                    start = number
                    i = i+6
                    finish = ""
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            finish += tokens[t][i]
                        i += 1
                    finish = int(finish)

                    j = int(start)
                    while j < finish:
                        individual_regex += chr(j) + "Γ"
                        j += 1
                    individual_regex +=  chr(finish)
                    temp = ""
                else:
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            number += tokens[t][i]
                        i += 1
                    number = int(number)
                    symbol = chr(number)
                    individual_regex += symbol
                    temp = ""
            i += 1
        
        if individual_regex[-1] in OPERATORS:
            individual_regex = individual_regex[:-1]
        if "CHR(" in individual_regex:
            individual_regex = individual_regex.replace('CHR(', 'Ꮸ')
        elif "(." in individual_regex:
            individual_regex = individual_regex.replace('(.', 'Ꮚ')
        elif ".)" in individual_regex:
            individual_regex = individual_regex.replace('.)', 'Ꮙ')
        tokens_parse_lines[t] = individual_regex
        if t == "charinterval":
            tokens_parse_lines[t] = 'ᏬᏨᏭᏜᏬᏬ0Γ1Γ2Γ3Γ4Γ5Γ6Γ7Γ8Γ9ᏭᏭᏜᏬᏬᏬ0Γ1Γ2Γ3Γ4Γ5Γ6Γ7Γ8Γ9ᏭᏭᏭΦᏜᏬ)ᏭᏜ.Ꮬ.ᏜᏬᏨᏭᏜᏬᏬ0Γ1Γ2Γ3Γ4Γ5Γ6Γ7Γ8Γ9ᏭᏭᏜᏬᏬᏬ0Γ1Γ2Γ3Γ4Γ5Γ6Γ7Γ8Γ9ᏭᏭᏭΦᏜᏬ)Ꮽ'
        elif t == "char":
            tokens_parse_lines[t] = "ᏬᏓᏭᏬᏬ/ᏭᏭΠᏬAΓBΓCΓDΓEΓFΓGΓHΓIΓJΓKΓLΓMΓNΓÑΓOΓPΓQΓRΓSΓTΓUΓVΓWΓXΓYΓZΓaΓbΓcΓdΓeΓfΓgΓhΓiΓjΓkΓlΓmΓnΓñΓoΓpΓqΓrΓsΓtΓuΓvΓwΓxΓyΓzᏭᏬᏓᏭ"
    return tokens_parse_lines

def make_tree(keyword_parse_lines, token_parse_lines):
    final_regex = ""
    dfas = {}
    if len(keyword_parse_lines) > 0:
        for keyword in keyword_parse_lines:
            final_regex += "Ꮼ" + keyword_parse_lines[keyword] + "Ꮽ" + "Γ"
            tree = generate_tree(keyword_parse_lines[keyword])
            dfas[keyword] = directo(tree, keyword_parse_lines[keyword])

    for token in token_parse_lines:
        print(token)
        final_regex += "Ꮼ" + token_parse_lines[token] +"Ꮽ" + "Γ"
        tree = generate_tree(token_parse_lines[token])
        dfas[token] = directo(tree, token_parse_lines[token])
    final_regex = final_regex[:-1]
    tree = generate_tree(final_regex)
    return dfas, final_regex

def make_one(dfas, final_regex):
    print(final_regex)
    tree = generate_tree(final_regex)
    final_dfa = directo(tree, final_regex)
    return final_dfa

def analyze(name, characters, keywords, tokens):
    character_parsed = analized_chars(characters)
    keyword_parsed = analyzed_keywords(keywords, character_parsed)
    token_parsed = analyzed_tokens(tokens, character_parsed)
    print("Characters parse:")
    print(character_parsed)
    print("Keywords parsed: ")
    print(keyword_parsed)
    print("Tokens parse:")
    print(token_parsed)

    dfas, final_regex = make_tree(keyword_parsed, token_parsed)
    final_dfa = make_one(dfas, final_regex)

   

    return final_dfa, dfas


