from parser import analyze
from scanner import scan
from generate_scanner import create

def main():
    print("archivo?")
    archivo = input()
    input_file = open("./input/" + archivo)
    data = input_file.read()
    input_file.close()
    name, characters, keywords, tokens= scan(data)
    final_dfa, dfas = analyze(name, characters, keywords, tokens)
    create(final_dfa, dfas, name)
    
if __name__ == "__main__":
    main()