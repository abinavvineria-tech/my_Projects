# timebreaker/cli/main.py
import argparse
import sys
import os
from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..interpreter.interpreter import Interpreter

def run_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()
    
    # Tokenize
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Parse
    parser = Parser(tokens)
    module = parser.parse()
    
    # Interpret
    interpreter = Interpreter()
    try:
        interpreter.interpret(module)
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)

def repl():
    print("TimeBreaker REPL (type 'exit' to quit)")
    interpreter = Interpreter()
    while True:
        try:
            source = input(">>> ")
            if source.strip() == "exit":
                break
            # Tokenize
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            # Parse
            parser = Parser(tokens)
            module = parser.parse()
            # Interpret
            result = interpreter.interpret(module)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="TimeBreaker programming language")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run a TimeBreaker file')
    run_parser.add_argument('file', help='Path to the TimeBreaker file')
    
    # repl command
    subparsers.add_parser('repl', help='Start the TimeBreaker REPL')
    
    # version command
    subparsers.add_parser('version', help='Print the version')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        run_file(args.file)
    elif args.command == 'repl':
        repl()
    elif args.command == 'version':
        print("TimeBreaker version 0.1.0")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()