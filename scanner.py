# Note: I've also added functionality of parenthesis and brackets for if and else statement.

import re

class TokenType:
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    OPERATOR = 'OPERATOR'
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    LITERAL = 'LITERAL'
    COMMENT = 'COMMENT'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'

class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

class Scanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def scan(self):
        source_code_lines = self.source_code.split('\n')
        for line in source_code_lines:
            line = line.strip()
            if line:
                self.tokenize_line(line)
        return self.tokens

    def tokenize_line(self, line):
        # Regular expressions for token patterns
        patterns = [
            (r'[0-9]+', TokenType.INTEGER),
            (r'true|false', TokenType.BOOLEAN),
            (r'\+|\-|\*|\/|\=|\=\=|\!\=', TokenType.OPERATOR),
            (r'if|else|print', TokenType.KEYWORD),
            (r'[a-zA-Z][a-zA-Z0-9]*', TokenType.IDENTIFIER),
            (r'//.*', TokenType.COMMENT),
            (r'\{', TokenType.LEFT_BRACE),
            (r'\}', TokenType.RIGHT_BRACE),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN)
        ]
        while line:
            for pattern, token_type in patterns:
                match = re.match(pattern, line)
                if match:
                    lexeme = match.group(0)
                    # Check for missing parentheses after "if" keyword
                    if token_type == TokenType.KEYWORD and lexeme == "if":
                        if not re.match(r'\(', line[len(lexeme):].strip()):
                            raise ValueError("Syntax error: Missing '(' after 'if'")
                    token = Token(token_type, lexeme)
                    self.tokens.append(token)
                    line = line[len(lexeme):].strip()
                    break
            else:
                raise ValueError("Invalid token at: " + line)

if __name__ == "__main__":
   # Read MiniLang source code from ino\put.txt file
    with open("input.txt", "r") as file:
        source_code = file.read()

    # Tokenize the source code
    scanner = Scanner(source_code)
    tokens = scanner.scan()

    # Print tokens + token type + lemxeme
    for token in tokens:
        print(f"Token Type: {token.token_type}, Lexeme: {token.lexeme}")