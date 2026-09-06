from timebreaker.lexer.lexer import Lexer

source = '''use std

aura name = "PureLily"
aura version = 1

spell greet(name):
    return "Hello, " + name

print(greet(name))
'''

lexer = Lexer(source)
tokens = lexer.tokenize()
for i, token in enumerate(tokens):
    print(f"{i:2}: {token.type} = {repr(token.value)}")