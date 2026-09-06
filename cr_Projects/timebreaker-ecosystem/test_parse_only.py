from timebreaker.lexer.lexer import Lexer
from timebreaker.parser.parser import Parser
from timebreaker.parser.ast import *

source = '''use std

aura name = "PureLily"
aura version = 1

spell greet(name):
    return "Hello, " + name

print(greet(name))
'''

print("Source:")
print(repr(source))

lexer = Lexer(source)
tokens = lexer.tokenize()
print("\nTokens:")
for i, token in enumerate(tokens):
    print(f"{i:2}: {token.type} = {repr(token.value)}")

parser = Parser(tokens)
module = parser.parse()
print("\nParsed module:")
print(module)
print("\nModule statements:")
for stmt in module.statements:
    print(f"  {stmt}")