# TimeBreaker × PureLily Studio Ecosystem

This is a prototype implementation of the TimeBreaker programming language and its ecosystem.

## What works

- **Lexer**: Tokenizes TimeBreaker source code.
- **Parser**: Parses tokens into an AST (supports imports, variable declarations, function definitions, print statements, if statements, expressions, etc.).
- **Interpreter**: Executes the AST, supports variables, functions, arithmetic, strings, booleans, conditionals, etc.
- **CLI**: `tb run <file>` to run a TimeBreaker script.
- **Package Manager Stub**: `tbpm` command (not fully implemented).
- **Example Programs**: 
  - `examples/hello.tb` - Prints "Hello, PureLily"
  - `examples/test.tb` - More complex example (currently times out due to parser issues with complex control flow, but the core works).

## How to run

1. Make sure you are in the `timebreaker-ecosystem` directory.
2. Run the hello world example:
   ```bash
   python -m timebreaker.cli.main run examples/hello.tb
   ```
   Output: `Hello, PureLily`

## Language Features Implemented

- Variables: `aura name = "value"`
- Functions: `spell func(params): ...`
- Print: `print("Hello")`
- Conditionals: `if condition: ... else: ...`
- Arithmetic: `+ - * / %`
- Comparison: `== != < > <= >=`
- Logical: `!` (not)
- Strings, integers, booleans
- Function calls and recursion (limited by interpreter stack)
- Imports: `use std` (currently ignored)

## Project Structure

```
timebreaker-ecosystem/
├── timebreaker/          # Language implementation
│   ├── lexer/            # Lexer
│   ├── parser/           # Parser and AST
│   ├── interpreter/      # Interpreter
│   └── cli/              # Command-line interface (tb and tbpm)
├── examples/             # Example TimeBreaker programs
├── docs/                 # Documentation (to be filled)
├── purelily-studio/      # Placeholder for the IDE (not implemented yet)
├── tbpm/                 # Package manager stub
└── scripts/              # Utility scripts
```

## Next Steps

To fully realize the vision from the original request, the following would need to be implemented:

1. **Complete the interpreter** to handle all language features (loops, etc.) without infinite loops.
2. **Implement the standard library** (`std.io`, `std.fs`, etc.).
3. **Build PureLily Studio** as a graphical IDE (could be a web-based or desktop app).
4. **Finish the package manager** (`tbpm`) with actual package installation, resolution, etc.
5. **Add debugging, testing, documentation generation** as described.
6. **Implement the AI assistant** (PureLily CodeMind).
7. **Add workspace and extension system**.

## Current Limitations

- The parser can get into infinite loops for certain constructs (like the test.tb example) due to left-recursion or other issues in the grammar.
- The interpreter does not yet support loops (`for`, `while`).
- The package manager is a stub.
- No IDE yet.

Despite these, the core of the language is functional and can run simple programs.

## Try it yourself

Edit `examples/hello.tb` or create a new `.tb` file and run it with `tb run`.

Enjoy exploring TimeBreaker!