from tree import generate_tree
from direct import directo
from utils import word_break

#documentacion from page 6 of pdf https://ssw.jku.at/Research/Projects/Coco/Doc/UserManual.pdf 
RESERVERD_KEYWORDS = ["ANY", "CHARACTERS", "COMMENTS", "COMPILER", "CONTEXT",
"END", "FROM", "IF", "IGNORE", "IGNORECASE", "NESTED", "out", "PRAGMAS",
"PRODUCTIONS", "SYNC", "TO", "TOKENS", "WEAK"]
OPERATORS = ['|', 'ξ'] #or y concatenacion nueva definicion para no entorpecer con el . de characters, tokens o mas

def analized_chars(characters):
    character_parsed = {}
    for c in characters:
        temp_string = ""
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
            elif temp_string + characters[c][i] in character_parsed:
                string_to_parse += character_parsed[temp_string+characters[c][i]]
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
    tokens_parse_lines = {}
    for t in tokens:
        token = tokens[t]
        i = 0
        temp = ""
        parse_line = ""
        flag = False
        while i < len(token):
            temp += token[i]
            if temp in characters:
                og = temp
                temp = word_break(token, characters, i, temp)
                if og != temp:
                    i += len(temp) - len(og)
                if flag:
                    parse_line += characters[temp] + ")*"
                else:
                    parse_line += characters[temp]
                temp = ""
            if "|" == temp:
                parse_line = parse_line[:-2] + "|"
                temp = ""
            if temp == "{":
                flag = not flag
                parse_line += "ξ("
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            if temp == "[":
                second_flag = True
                if parse_line != "":
                    parse_line += "ξ"
                parse_line += "("
                temp = ""
            if temp == "]":
                second_flag = False
                parse_line += "?"
                temp = ""
            if temp == '"':
                inner = ""
                i += 1
                while i < len(token):
                    if token[i] == '"':
                        break
                    inner += token[i]
                    i += 1
                if parse_line != "" :
                    parse_line += "ξ(" + inner + ")"
                else:
                    parse_line += "(" + inner + ")"
                if token[i + 1] != "" and token[i + 1] != "\n" and token[i + 1] != ".":
                    parse_line += "ξ"
                temp = ""
            if temp == "(":
                parse_line += "("
                temp = ""
            if temp == ")":
                parse_line += ")"
                temp = ""
            i += 1
        if parse_line[-1] in OPERATORS:
            parse_line = parse_line[:-1]
        tokens_parse_lines[t] = parse_line
    return tokens_parse_lines

def make_tree(keyword_parse_lines, token_parse_lines):
    complete_line = ""
    dfas = {}
    for keyword in keyword_parse_lines:
        complete_line += "(" + keyword_parse_lines[keyword] + ")" + "|"
        tree = generate_tree(keyword_parse_lines[keyword])
        dfas[keyword] = directo(tree, keyword_parse_lines[keyword])
    for token in token_parse_lines:
        complete_line += "(" + token_parse_lines[token] +")" + "|"
        tree = generate_tree(token_parse_lines[token])
        dfas[token] = directo(tree, token_parse_lines[token])
    complete_line = complete_line[:-1]
    tree = generate_tree(complete_line)
    return dfas, complete_line

def make_one(dfas, complete_line):
    tree = generate_tree(complete_line)
    final_dfa = directo(tree, complete_line)
    return final_dfa

def analyze(name, characters, keywords, tokens):
    character_parse_lines = analized_chars(characters)
    keyword_parse_lines = analyzed_keywords(keywords, character_parse_lines)
    token_parse_lines = analyzed_tokens(tokens, character_parse_lines)
    dfas, complete_line = make_tree(keyword_parse_lines, token_parse_lines)
    final_dfa = make_one(dfas, complete_line)
    return final_dfa, dfas


