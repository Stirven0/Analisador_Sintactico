# Definimos los tipos de tokens
TOKEN_TYPES = {
    'NUMBER': 'NUMBER',
    'IDENTIFIER': 'IDENTIFIER',
    'OPERATOR': 'OPERATOR',
    'PARENTHESIS': 'PARENTHESIS',
    'EOF': 'EOF',  # End of file (fin de entrada)
}

class Lexer:
    def __init__(self, input_string):
        self.input = input_string
        self.position = 0
        self.current_char = self.input[self.position] if self.input else None

    def advance(self):
        """Mueve la posición un carácter hacia adelante."""
        self.position += 1
        if self.position >= len(self.input):
            self.current_char = None  # Señala el fin de la entrada
        else:
            self.current_char = self.input[self.position]

    def skip_whitespace(self):
        """Ignora los espacios en blanco."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Reconoce un número."""
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return {'type': TOKEN_TYPES['NUMBER'], 'value': int(num_str)}

    def identifier(self):
        """Reconoce un identificador (letras o guiones bajos)."""
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        return {'type': TOKEN_TYPES['IDENTIFIER'], 'value': id_str}

    def get_next_token(self):
        """Obtiene el siguiente token de la entrada."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char in '+-*/=':
                token = {'type': TOKEN_TYPES['OPERATOR'], 'value': self.current_char}
                self.advance()
                return token

            if self.current_char in '()':
                token = {'type': TOKEN_TYPES['PARENTHESIS'], 'value': self.current_char}
                self.advance()
                return token

            raise Exception(f'Error léxico: carácter no reconocido "{self.current_char}"')

        return {'type': TOKEN_TYPES['EOF'], 'value': None}

def main():
    input_string = "x = 3 + 5 * (10 - 4)"
    lexer = Lexer(input_string)

    while True:
        token = lexer.get_next_token()
        if token['type'] == TOKEN_TYPES['EOF']:
            break
        print(token)

if __name__ == '__main__':
    main()
