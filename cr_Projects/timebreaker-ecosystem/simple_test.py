import sys
sys.path.insert(0, '.')

from timebreaker.lexer.lexer import Lexer
from timebreaker.parser.parser import Parser

# Test a very simple program
source = "aura x = 1"
print("Source:", repr(source))
lexer = Lexer(source)
tokens = lexer.tokenize()
print("Tokens:", len(tokens))
for t in tokens:
    print(t)

print("\nParsing...")
parser = Parser(tokens)
module = parser.parse()
print("Parsed module:", module)