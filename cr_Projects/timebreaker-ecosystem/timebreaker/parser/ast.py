class ASTNode:
    pass

class Module(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Import(ASTNode):
    def __init__(self, module):
        self.module = module

class VariableDeclaration(ASTNode):
    def __init__(self, name, value, is_constant=False):
        self.name = name
        self.value = value
        self.is_constant = is_constant

class FunctionDeclaration(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class ExpressionStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class NumericLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class CallExpression(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class PrintStatement(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch  # list of statements
        self.else_branch = else_branch  # list of statements or None