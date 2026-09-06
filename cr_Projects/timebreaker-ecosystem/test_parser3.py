import sys
sys.path.insert(0, '.')

from timebreaker.lexer.lexer import Lexer, TokenType
from timebreaker.parser.parser import Parser
from timebreaker.parser.ast import *

def test_parse(source):
    print("Parsing source:")
    print(repr(source))
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print(f"Number of tokens: {len(tokens)}")
    # Print first few tokens
    for i, token in enumerate(tokens[:10]):
        print(f"  {i}: {token}")
    if len(tokens) > 10:
        print("  ...")
    parser = Parser(tokens)
    try:
        module = parser.parse()
        print("Parsing succeeded!")
        # Optionally, we can print the AST here, but for now just return success.
        return True
    except Exception as e:
        print(f"Parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 1: simple variable
test1 = "aura x = 1"
print("="*50)
test_parse(test1)

# Test 2: function
test2 = """
spell greet(name):
    return "Hello, " + name
"""
print("="*50)
test_parse(test2)

# Test 3: the hello world example
with open('examples/hello.tb', 'r') as f:
    test3 = f.read()
print("="*50)
test_parse(test3)