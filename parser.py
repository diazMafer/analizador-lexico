from automatas import tree
from automatas import direct
import utils

#documentacion from page 6 of pdf https://ssw.jku.at/Research/Projects/Coco/Doc/UserManual.pdf 
RESERVERD_KEYWORDS = ["ANY", "CHARACTERS", "COMMENTS", "COMPILER", "CONTEXT",
"END", "FROM", "IF", "IGNORE", "IGNORECASE", "NESTED", "out", "PRAGMAS",
"PRODUCTIONS", "SYNC", "TO", "TOKENS", "WEAK"]
OPERATORS = ['|', 'ξ'] #or y concatenacion nueva definicion para no entorpecer con el . de characters, tokens o mas

def analized_chars(characters):
    chars_parsed = {}
    for c in characters:
        string = ""
        flag = False
        i = 0
        string_to_parse = ""
        while i < len(characters[c]):
            if characters[c][i] == '"' or characters[c][i] == "'":
                flag = not flag
                if not flag:
                    temp_string = temp_string[:-1] + ")"
                    string_to_parse += temp_string
                    string_to_parse = ""
                else:
                    temp_string += "("
            elif flag:
                temp_string += characters[c][i] + "|"
            elif characters[c][i] == "+":
                string_to_parse += "|"
            elif temp_string + characters[c][i] in characters_parsed:
                string_to_parse += characters_parsed[temp_string+characters[c][i]]
                temp_string = ""
            elif temp_string == ".":
                if characters[c][i] == ".":
                    start = string_to_parse[-2]
                    finish = ""
                    while i < len(characters[c]):
                        if characters[c][i] == "'":
                            break
                        i += 1
                    finish = characters[c][i + 1]
                    j = ord(start)
                    while j < ord(finish):
                        string_to_parse += "|" + chr(j)
                        j += 1
                    string_to_parse += "|" + finish
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
                string_to_parse += "'"+symbol+"'"
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parsed[c] = "(" +  string_to_parse + ")"
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
                    temp = temp[:-1] +  ")"
                else:
                    temp += "("
            else:
                temp += word[i] + "ξ"
            i += 1
        keywords_parsed[k] = temp
    return keywords_parsed

def analyzed_tokens(tokens, characters):
    tokens_parse = {}








