
class Parser:
    file_path : str

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self._parse_line(file)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} does not exist")
        except IOError:
            print(f"Error: An I/O error occurred when reading the file at '{self.file_path}'")

    def _parse_line(self, file):
        for line in file:
            print(line.strip())