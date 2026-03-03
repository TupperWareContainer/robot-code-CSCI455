from al_dialog_tokenizer import Tokenizer
from al_dialog_parser import Parser

def main():
    tokenizer = Tokenizer("./testDialogFileForPractice.txt")
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

if __name__ == '__main__':
    main()