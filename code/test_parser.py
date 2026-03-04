from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser

def main():
    path = "./testDialogFileForPractice.txt"
    tokenizer = Tokenizer(path)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens, path)
    program = parser.parse()

if __name__ == '__main__':
    main()