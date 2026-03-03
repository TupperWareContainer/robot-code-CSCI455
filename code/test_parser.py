from robot_tokenizer import Tokenizer
from robot_parser import Parser

def main():
    tokenizer = Tokenizer("./testDialogFileForPractice.txt")
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

if __name__ == '__main__':
    main()