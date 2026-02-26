
class Tokenizer:
    file_path : str

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self._tokenize_line(file)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} does not exist")
        except IOError:
            print(f"Error: An I/O error occurred when reading the file at '{self.file_path}'")

    def _tokenize_line(self, file):
        for line in file:
            stripped_line = line.strip()

            for token in stripped_line:
                if token == '#':
                    continue
                elif token == '"':
                    self._tokenize_str()
                elif token == '&':
                    pass


    def _tokenize_str(self):
        pass