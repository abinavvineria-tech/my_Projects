import tokenize
import io
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    USE = 'use'
    AURA = 'aura'
    SPELL = 'spell'
    RETURN = 'return'
    PRINT = 'print'  # Add print as a keyword
    IF = 'if'
    ELSE = 'else'
    FOR = 'for'
    WHILE = 'while'
    # We are using indentation for blocks, so we don't need BATTLE as a keyword? But let's keep it in case we want to use it explicitly.
    BATTLE = 'battle'
    CLASS = 'class'
    NEW = 'new'
    TRY = 'try'
    CATCH = 'catch'
    ASYNC = 'async'
    AWAIT = 'await'
    MATCH = 'match'
    BREAK = 'break'
    CONTINUE = 'continue'
    # Literals
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    BOOLEAN = 'BOOLEAN'
    # Identifiers
    IDENTIFIER = 'IDENTIFIER'
    # Operators and delimiters
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    PERCENT = '%'
    EQUAL = '='
    EQUAL_EQUAL = '=='
    BANG = '!'
    BANG_EQUAL = '!='
    LESS_THAN = '<'
    GREATER_THAN = '>'
    LESS_EQUAL = '<='
    GREATER_EQUAL = '>='
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    LBRACKET = '['
    RBRACKET = ']'
    COMMA = ','
    COLON = ':'
    DOT = '.'
    # Indentation
    INDENT = 'INDENT'
    DEDENT = 'DEDENT'
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line}, column={self.column})'

class Lexer:
    def __init__(self, source):
        self.source = source
        self.source_io = io.StringIO(source)

    def tokenize(self):
        tokens = []
        try:
            for token in tokenize.generate_tokens(self.source_io.readline):
                # token is a tuple: (type, string, start, end, line)
                token_type = token[0]
                token_string = token[1]
                start_line, start_column = token[2]
                # We will map the token type to our TokenType
                our_type = self.map_token_type(token_type, token_string)
                if our_type is None:
                    # Skip this token (e.g., COMMENT, NL)
                    continue
                # For literals, we might need to process the value
                value = self.process_literal(our_type, token_string)
                if our_type in (TokenType.INDENT, TokenType.DEDENT):
                    value = None
                tokens.append(Token(our_type, value, start_line, start_column))
        except tokenize.TokenError as e:
            raise Exception(f"Tokenization error: {e}")
        # We don't add an extra EOF because ENDMARKER gives us that.
        return tokens

    def map_token_type(self, token_type, token_string):
        if token_type == tokenize.NAME:
            if token_string == 'use':
                return TokenType.USE
            elif token_string == 'aura':
                return TokenType.AURA
            elif token_string == 'spell':
                return TokenType.SPELL
            elif token_string == 'return':
                return TokenType.RETURN
            elif token_string == 'print':
                return TokenType.PRINT
            elif token_string == 'if':
                return TokenType.IF
            elif token_string == 'else':
                return TokenType.ELSE
            elif token_string == 'for':
                return TokenType.FOR
            elif token_string == 'while':
                return TokenType.WHILE
            elif token_string == 'battle':
                return TokenType.BATTLE
            elif token_string == 'class':
                return TokenType.CLASS
            elif token_string == 'new':
                return TokenType.NEW
            elif token_string == 'try':
                return TokenType.TRY
            elif token_string == 'catch':
                return TokenType.CATCH
            elif token_string == 'async':
                return TokenType.ASYNC
            elif token_string == 'await':
                return TokenType.AWAIT
            elif token_string == 'match':
                return TokenType.MATCH
            elif token_string == 'break':
                return TokenType.BREAK
            elif token_string == 'continue':
                return TokenType.CONTINUE
            elif token_string == 'true':
                return TokenType.BOOLEAN
            elif token_string == 'false':
                return TokenType.BOOLEAN
            else:
                return TokenType.IDENTIFIER
        elif token_type == tokenize.NUMBER:
            # We'll try to parse as integer if possible, otherwise float
            if '.' in token_string or 'e' in token_string or 'E' in token_string:
                return TokenType.FLOAT
            else:
                return TokenType.INTEGER
        elif token_type == tokenize.STRING:
            return TokenType.STRING
        elif token_type == tokenize.OP:
            # Map operators and delimiters
            if token_string == '+':
                return TokenType.PLUS
            elif token_string == '-':
                return TokenType.MINUS
            elif token_string == '*':
                return TokenType.STAR
            elif token_string == '/':
                return TokenType.SLASH
            elif token_string == '%':
                return TokenType.PERCENT
            elif token_string == '=':
                return TokenType.EQUAL
            elif token_string == '==':
                return TokenType.EQUAL_EQUAL
            elif token_string == '!':
                return TokenType.BANG
            elif token_string == '!=':
                return TokenType.BANG_EQUAL
            elif token_string == '<':
                return TokenType.LESS_THAN
            elif token_string == '>':
                return TokenType.GREATER_THAN
            elif token_string == '<=':
                return TokenType.LESS_EQUAL
            elif token_string == '>=':
                return TokenType.GREATER_EQUAL
            elif token_string == '(':
                return TokenType.LPAREN
            elif token_string == ')':
                return TokenType.RPAREN
            elif token_string == '{':
                return TokenType.LBRACE
            elif token_string == '}':
                return TokenType.RBRACE
            elif token_string == '[':
                return TokenType.LBRACKET
            elif token_string == ']':
                return TokenType.RBRACKET
            elif token_string == ',':
                return TokenType.COMMA
            elif token_string == ':':
                return TokenType.COLON
            elif token_string == '.':
                return TokenType.DOT
            else:
                # We don't know this operator, we'll treat it as an identifier? Or raise an error?
                # For now, we'll return IDENTIFIER, but this might cause issues.
                return TokenType.IDENTIFIER
        elif token_type == tokenize.INDENT:
            return TokenType.INDENT
        elif token_type == tokenize.DEDENT:
            return TokenType.DEDENT
        elif token_type == tokenize.NEWLINE:
            return TokenType.NEWLINE
        elif token_type == tokenize.ENDMARKER:
            return TokenType.EOF
        else:
            # For other token types (like COMMENT, NL), we will ignore them by returning None
            return None

    def process_literal(self, token_type, token_string):
        if token_type == TokenType.STRING:
            # Remove the quotes (both single and double quotes)
            if len(token_string) >= 2 and (
                (token_string[0] == '"' and token_string[-1] == '"') or
                (token_string[0] == "'" and token_string[-1] == "'")
            ):
                return token_string[1:-1]
            return token_string
        elif token_type == TokenType.INTEGER:
            return int(token_string)
        elif token_type == TokenType.FLOAT:
            return float(token_string)
        elif token_type == TokenType.BOOLEAN:
            return token_string == 'true'
        else:
            # For other tokens, the value is the string itself (e.g., for keywords, identifiers, operators)
            return token_string