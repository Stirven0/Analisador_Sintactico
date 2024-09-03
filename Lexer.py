import argparse

# Definimos los tipos de tokens
TOKEN_TYPES = {
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    'BOOLEAN': 'BOOLEAN',
    'NULL': 'NULL',
    'IDENTIFIER': 'IDENTIFIER',
    'OPERATOR': 'OPERATOR',
    'RELATIONAL': 'RELATIONAL',
    'ASSIGNMENT': 'ASSIGNMENT',
    'DELIMITERS': 'DELIMITERS',
    'COMMENT': 'COMMENT',
    'EOF': 'EOF',
    'KEYWORD': 'KEYWORD',
    'INDENT': 'INDENT',
    'DEDENT': 'DEDENT',
    'MEMBER_ACCESS': 'MEMBER_ACCESS'
}

# Definimos las palabras clave
KEYWORDS = {
    'if', 'else', 'while', 'for', 'none', 'null', 'def', 'class', 'return', 'import'
}

# Definimos los literales booleanos y nulos
BOOLEAN_LITERALS = {'True', 'False'}
NULL_LITERAL = {'null', 'none'}

# Definimos los operadores lógicos
LOGICAL_OPERATORS = {'and', 'or', 'not'}

# Definimos los operadores relacionales
RELATIONAL_OPERATORS = {'==', '!=', '<=', '>=', '<', '>'}

# Definimos los operadores de asignación
ASSIGNMENT_OPERATORS = {'=', '+=', '-=', '*=', '/='}

class Lexer:
    def __init__(self, input_string):
        self.input = input_string
        self.position = 0
        self.current_char = self.input[self.position] if self.input else None
        self.indent_stack = [0]

    def advance(self):
        """Mueve la posición un carácter hacia adelante."""
        self.position += 1
        if self.position >= len(self.input):
            self.current_char = None
        else:
            self.current_char = self.input[self.position]

    def peek(self):
        """Devuelve el siguiente carácter sin avanzar la posición."""
        peek_pos = self.position + 1
        if peek_pos >= len(self.input):
            return None
        return self.input[peek_pos]

    def skip_whitespace(self):
        """Ignora los espacios en blanco."""
        while self.current_char is not None and self.current_char.isspace() and self.current_char not in '\n\t':
            self.advance()

    def number(self):
        """Reconoce un número."""
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return {'type': TOKEN_TYPES['NUMBER'], 'value': int(num_str)}

    def string(self, quote_type):
        """Reconoce una cadena de texto."""
        string_val = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != quote_type:
            string_val += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return {'type': TOKEN_TYPES['STRING'], 'value': string_val}

    def identifier_or_literal(self):
        """Reconoce un identificador, palabra clave, booleano o nulo."""
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return {'type': TOKEN_TYPES['KEYWORD'], 'value': id_str}
        elif id_str in LOGICAL_OPERATORS:
            return {'type': TOKEN_TYPES['OPERATOR'], 'value': id_str}
        elif id_str in BOOLEAN_LITERALS:
            return {'type': TOKEN_TYPES['BOOLEAN'], 'value': id_str}
        elif id_str in NULL_LITERAL:
            return {'type': TOKEN_TYPES['NULL'], 'value': None}
        else:
            return {'type': TOKEN_TYPES['IDENTIFIER'], 'value': id_str}

    def handle_indent_dedent(self):
        """Maneja las indentaciones y dedentaciones al comienzo de una línea."""
        indent_level = 0
        while self.current_char == ' ' or self.current_char == '\t':
            if self.current_char == ' ':
                indent_level += 1
            elif self.current_char == '\t':
                indent_level += 4
            self.advance()

        last_indent = self.indent_stack[-1]

        if indent_level > last_indent:
            self.indent_stack.append(indent_level)
            return {'type': TOKEN_TYPES['INDENT'], 'value': indent_level}
        elif indent_level < last_indent:
            tokens = []
            while indent_level < self.indent_stack[-1]:
                self.indent_stack.pop()
                tokens.append({'type': TOKEN_TYPES['DEDENT'], 'value': self.indent_stack[-1]})
            return tokens

        return None

    def relational_operator(self):
        """Reconoce un operador relacional."""
        rel_op_str = self.current_char
        if self.peek() in ('=', '<', '>'):
            rel_op_str += self.peek()
            self.advance()
        self.advance()
        return {'type': TOKEN_TYPES['RELATIONAL'], 'value': rel_op_str}

    def assignment_operator(self):
        """Reconoce un operador de asignación."""
        assign_op_str = self.current_char
        if self.peek() == '=':
            assign_op_str += self.peek()
            self.advance()
        self.advance()
        return {'type': TOKEN_TYPES['ASSIGNMENT'], 'value': assign_op_str}

    def comment(self):
        """Reconoce un comentario."""
        comment_str = ''
        while self.current_char is not None and self.current_char != '\n':
            comment_str += self.current_char
            self.advance()
        return {'type': TOKEN_TYPES['COMMENT'], 'value': comment_str}

    def get_next_token(self):
        """Obtiene el siguiente token de la entrada."""
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':
                    self.advance()
                    if self.current_char == ' ' or self.current_char == '\t':
                        indent_token = self.handle_indent_dedent()
                        if indent_token:
                            return indent_token
                else:
                    self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_literal()

            if self.current_char in '+-*/':
                if self.peek() == '=':
                    return self.assignment_operator()
                else:
                    token = {'type': TOKEN_TYPES['OPERATOR'], 'value': self.current_char}
                    self.advance()
                    return token

            if self.current_char == '=':
                if self.peek() == '=':
                    return self.relational_operator()
                else:
                    return self.assignment_operator()

            if self.current_char in '!<>':
                return self.relational_operator()

            if self.current_char in '(){}[],:.':
                if self.current_char == '.':
                    token = {'type': TOKEN_TYPES['MEMBER_ACCESS'], 'value': self.current_char}
                else:
                    token = {'type': TOKEN_TYPES['DELIMITERS'], 'value': self.current_char}
                self.advance()
                return token

            if self.current_char == '\'' or self.current_char == '\"':
                return self.string(self.current_char)

            if self.current_char == '#':
                return self.comment()

            raise Exception(f'Error léxico: carácter no reconocido "{self.current_char}"')

        return {'type': TOKEN_TYPES['EOF'], 'value': None}

def main():
    parser = argparse.ArgumentParser(description='Lexer')
    parser.add_argument('-f', '--file', type=str, help='Archivo a procesar')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            input_string = file.read()
    else:
        input_string = input("Ingrese el código a analizar: ")

    lexer = Lexer(input_string)

    while True:
        token = lexer.get_next_token()
        if isinstance(token, list):
            for t in token:
                print(t)
                if t['type'] == TOKEN_TYPES['EOF']:
                    return
        else:
            print(token)
            if token['type'] == TOKEN_TYPES['EOF']:
                break

if __name__ == '__main__':
    main()
