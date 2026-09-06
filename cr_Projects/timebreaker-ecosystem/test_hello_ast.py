from timebreaker.lexer.lexer import Lexer
from timebreaker.parser.parser import Parser
from timebreaker.parser.ast import *

with open('examples/hello.tb', 'r') as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()
print("Tokens:")
for i, token in enumerate(tokens):
    print(f"{i:2}: {token}")

print("\n---\n")

parser = Parser(tokens)
module = parser.parse()

print("AST:")
def print_ast(node, indent=0):
    spaces = "  " * indent
    if isinstance(node, Module):
        print(f"{spaces}Module")
        for stmt in node.statements:
            print_ast(stmt, indent+1)
    elif isinstance(node, Import):
        print(f"{spaces}Import: {node.module}")
    elif isinstance(node, VariableDeclaration):
        print(f"{spaces}VariableDeclaration: {node.name} = {node.value} (const={node.is_constant})")
    elif isinstance(node, FunctionDeclaration):
        print(f"{spaces}FunctionDeclaration: {node.name}({', '.join(node.params)})")
        print(f"{spaces}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent+2)
    elif isinstance(node, ExpressionStatement):
        print(f"{spaces}ExpressionStatement:")
        print_ast(node.expression, indent+1)
    elif isinstance(node, BinaryExpression):
        print(f"{spaces}BinaryExpression: {node.operator}")
        print(f"{spaces}  Left:")
        print_ast(node.left, indent+1)
        print(f"{spaces}  Right:")
        print_ast(node.right, indent+1)
    elif isinstance(node, UnaryExpression):
        print(f"{spaces}UnaryExpression: {node.operator}")
        print(f"{spaces}  Operand:")
        print_ast(node.operand, indent+1)
    elif isinstance(node, StringLiteral):
        print(f"{spaces}StringLiteral: {repr(node.value)}")
    elif isinstance(node, NumericLiteral):
        print(f"{spaces}NumericLiteral: {node.value}")
    elif isinstance(node, BooleanLiteral):
        print(f"{spaces}BooleanLiteral: {node.value}")
    elif isinstance(node, Identifier):
        print(f"{spaces}Identifier: {node.name}")
    elif isinstance(node, ReturnStatement):
        print(f"{spaces}ReturnStatement:")
        print_ast(node.value, indent+1)
    else:
        print(f"{spaces}Unknown: {type(node)}")

print_ast(module)