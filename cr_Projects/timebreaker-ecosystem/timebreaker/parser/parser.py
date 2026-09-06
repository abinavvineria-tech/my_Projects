from ..lexer.lexer import TokenType, Token
from .ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        if self.is_at_end():
            return Module([])
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        return Module(statements)

    def declaration(self):
        # Handle EOF first
        if self.match(TokenType.EOF):
            return None
        # Skip newlines
        if self.match(TokenType.NEWLINE):
            return None
        if self.match(TokenType.USE):
            return self.import_declaration()
        if self.match(TokenType.AURA):
            return self.variable_declaration()
        if self.match(TokenType.SPELL):
            return self.function_declaration()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def import_declaration(self):
        module = self.consume_identifier().value
        return Import(module)

    def variable_declaration(self):
        name = self.consume_identifier().value
        value = None
        if self.match(TokenType.EQUAL):
            value = self.expression()
        # For now, all aura declarations are variables (not constants)
        return VariableDeclaration(name, value, is_constant=False)

    def function_declaration(self):
        name = self.consume_identifier().value
        self.consume(TokenType.LPAREN)
        params = []
        if not self.check(TokenType.RPAREN):
            params.append(self.consume_identifier().value)
            while self.match(TokenType.COMMA):
                params.append(self.consume_identifier().value)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.COLON)
        self.consume(TokenType.NEWLINE)
        self.consume(TokenType.INDENT)
        body = self.block()
        # The block function already consumed the matching DEDENT
        return FunctionDeclaration(name, params, body)

    def block(self):
        statements = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        if self.check(TokenType.DEDENT):
            self.consume(TokenType.DEDENT)
        return statements

    def expression_statement(self):
        expr = self.expression()
        if expr is None:
            return None
        return ExpressionStatement(expr)

    def print_statement(self):
        # Consume the PRINT token (already consumed by match)
        # Expect a left parenthesis
        self.consume(TokenType.LPAREN)
        # Parse the expressions inside the parentheses, separated by commas
        expressions = []
        if not self.check(TokenType.RPAREN):
            expressions.append(self.expression())
            while self.match(TokenType.COMMA):
                expressions.append(self.expression())
        # Expect a right parenthesis
        self.consume(TokenType.RPAREN)
        return PrintStatement(expressions)

    def if_statement(self):
        # IF token already consumed
        condition = self.expression()
        self.consume(TokenType.COLON)
        self.consume(TokenType.NEWLINE)
        self.consume(TokenType.INDENT)
        then_branch = self.block()
        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.COLON)
            self.consume(TokenType.NEWLINE)
            self.consume(TokenType.INDENT)
            else_branch = self.block()
        return IfStatement(condition, then_branch, else_branch)

    def return_statement(self):
        # RETURN token already consumed by match in declaration
        value = None
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.DEDENT):
            value = self.expression()
        return ReturnStatement(value)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL) or self.match(TokenType.BANG_EQUAL):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryExpression(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.LESS_THAN) or self.match(TokenType.GREATER_THAN) or \
              self.match(TokenType.LESS_EQUAL) or self.match(TokenType.GREATER_EQUAL):
            operator = self.previous().value
            right = self.term()
            expr = BinaryExpression(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            operator = self.previous().value
            right = self.factor()
            expr = BinaryExpression(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR) or self.match(TokenType.SLASH) or self.match(TokenType.PERCENT):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryExpression(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS) or self.match(TokenType.BANG):
            operator = self.previous().value
            right = self.unary()
            return UnaryExpression(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.BOOLEAN):
            value = self.previous().value
            return BooleanLiteral(value)
        if self.match(TokenType.STRING):
            value = self.previous().value
            return StringLiteral(value)
        if self.match(TokenType.INTEGER):
            value = self.previous().value
            return NumericLiteral(value)
        if self.match(TokenType.FLOAT):
            value = self.previous().value
            return NumericLiteral(value)
        if self.match(TokenType.IDENTIFIER):
            name = self.previous().value
            # Check if this is a function call
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.consume(TokenType.RPAREN)
                return CallExpression(Identifier(name), args)
            return Identifier(name)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN)
            return expr
        # If we get here, it's an error. We'll just return None for now.
        # In a real parser, we would report an error.
        return None

    # Helper methods
    def is_at_end(self):
        return self.current >= len(self.tokens)

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        if self.is_at_end():
            return self.tokens[-1]
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        return False

    def consume(self, token_type):
        if self.check(token_type):
            return self.advance()
        # We'll just raise an exception for now. In a real parser, we'd report an error and try to recover.
        raise Exception(f"Expected {token_type} but got {self.peek().type}")

    def consume_identifier(self):
        if self.check(TokenType.IDENTIFIER):
            return self.advance()
        raise Exception("Expected identifier")