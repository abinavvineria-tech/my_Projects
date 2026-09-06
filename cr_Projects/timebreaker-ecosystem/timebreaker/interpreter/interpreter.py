from ..parser.ast import *

class Interpreter:
    def __init__(self):
        self.globals = {}  # global scope
        self.locals = [self.globals]  # stack of scopes, starts with global scope
        self.return_value = None

    def interpret(self, module):
        self.execute_block(module.statements)
        return self.return_value

    def execute_block(self, statements):
        # Push a new scope for the block
        self.locals.append({})
        try:
            for statement in statements:
                self.execute_statement(statement)
        finally:
            # Pop the scope
            self.locals.pop()

    def execute_statement(self, statement):
        if isinstance(statement, Import):
            self.execute_import(statement)
        elif isinstance(statement, VariableDeclaration):
            self.execute_variable_declaration(statement)
        elif isinstance(statement, FunctionDeclaration):
            self.execute_function_declaration(statement)
        elif isinstance(statement, ExpressionStatement):
            self.execute_expression_statement(statement)
        elif isinstance(statement, ReturnStatement):
            self.execute_return_statement(statement)
        elif isinstance(statement, PrintStatement):
            self.execute_print_statement(statement)
        elif isinstance(statement, IfStatement):
            self.execute_if_statement(statement)
        else:
            raise Exception(f"Unknown statement type: {type(statement)}")

    def execute_import(self, stmt):
        # For now, we ignore imports. In a real system, we would load the module.
        pass

    def execute_variable_declaration(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        # Find the scope to put the variable in: the innermost scope
        self.locals[-1][stmt.name] = value

    def execute_function_declaration(self, stmt):
        # Create a function object: (declaration, closure)
        # closure is the current stack of scopes (list of dicts)
        closure = list(self.locals)  # copy the list of scopes
        func = (stmt, closure)
        # Store the function in the current scope
        self.locals[-1][stmt.name] = func

    def execute_expression_statement(self, stmt):
        self.evaluate(stmt.expression)

    def execute_return_statement(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        self.return_value = value
        # Use an exception to unwind the stack
        raise ReturnException(value)

    def execute_print_statement(self, stmt):
        # Evaluate each expression and print them separated by a space
        values = [self.evaluate(expr) for expr in stmt.expressions]
        # Convert to string and join with a space
        print(' '.join(str(v) for v in values))

    def execute_if_statement(self, stmt):
        condition_value = self.evaluate(stmt.condition)
        if condition_value:
            self.execute_block(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute_block(stmt.else_branch)

    def evaluate(self, expr):
        if isinstance(expr, BinaryExpression):
            return self.evaluate_binary(expr)
        elif isinstance(expr, UnaryExpression):
            return self.evaluate_unary(expr)
        elif isinstance(expr, StringLiteral):
            return expr.value
        elif isinstance(expr, NumericLiteral):
            return expr.value
        elif isinstance(expr, BooleanLiteral):
            return expr.value
        elif isinstance(expr, Identifier):
            return self.look_up_variable(expr.name)
        elif isinstance(expr, CallExpression):
            return self.evaluate_call(expr)
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")

    def evaluate_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator == '+':
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise Exception("Operands must be two numbers or two strings.")
        elif expr.operator == '-':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left - right
        elif expr.operator == '*':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left * right
        elif expr.operator == '/':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left / right
        elif expr.operator == '%':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left % right
        elif expr.operator == '==':
            return left == right
        elif expr.operator == '!=':
            return left != right
        elif expr.operator == '<':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left < right
        elif expr.operator == '>':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left > right
        elif expr.operator == '<=':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left <= right
        elif expr.operator == '>=':
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Operands must be numbers.")
            return left >= right
        else:
            raise Exception(f"Unknown binary operator: {expr.operator}")

    def evaluate_unary(self, expr):
        right = self.evaluate(expr.operand)
        if expr.operator == '-':
            if not isinstance(right, (int, float)):
                raise Exception("Operand must be a number.")
            return -right
        elif expr.operator == '!':
            return not bool(right)
        else:
            raise Exception(f"Unknown unary operator: {expr.operator}")

    def look_up_variable(self, name):
        # Check scopes from innermost to outermost
        for scope in reversed(self.locals):
            if name in scope:
                return scope[name]
        # If not found, raise an error
        raise Exception(f"Undefined variable '{name}'.")

    def evaluate_call(self, expr):
        # expr.callee should be a function value: (declaration, closure)
        callee = self.evaluate(expr.callee)
        if not isinstance(callee, tuple) or len(callee) != 2:
            raise Exception("Can only call functions.")
        decl, closure = callee
        # Push the closure scopes onto the stack
        for scope in closure:
            self.locals.append(scope)
        # Push a new scope for the function's local variables
        self.locals.append({})
        # Define parameters
        for i, param in enumerate(decl.params):
            if i < len(expr.arguments):
                arg_value = self.evaluate(expr.arguments[i])
                self.locals[-1][param] = arg_value
            else:
                self.locals[-1][param] = None  # default to None
        try:
            self.execute_block(decl.body)
        except ReturnException as e:
            # Pop the function locals and the closure scopes
            self.locals.pop()  # function locals
            for _ in closure:
                self.locals.pop()  # each closure scope
            return e.value
        # If no return, still pop the scopes
        self.locals.pop()  # function locals
        for _ in closure:
            self.locals.pop()  # closure scopes
        return None


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()