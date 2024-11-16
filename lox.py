import sys
from lox.astprinter import AstPrinter
from lox.interpreter import Interpreter
from lox.parser import Parser
from lox.scanner import Scanner
from lox.tokentype import TokenType


def runtimeerror(error):
    # todo: Refactor. See Chapter evaluating expressions.
    print(error.args[1] + '\n[line ' +
          str(error.args[0].line) + ']', file=sys.stderr)
    global hadruntimeerror
    hadruntimeerror = True


interpreter = Interpreter(runtimeerror)
haderror = False
hadruntimeerror = False


def main():
    if len(sys.argv) > 2:
        print('Usage: plox [script]')
        sys.exit(64)
    elif len(sys.argv) == 2:
        __runfile(sys.argv[1])
    else:
        __runprompt()


def __runfile(path):
    with open(path) as f:
        __run(f.readall())

        if haderror:
            sys.exit(65)
        if hadruntimeerror:
            sys.exit(70)


def __runprompt():
    try:
        while True:
            print('> ', end='')
            line = input()
            if line == '':
                break
            __run(line)
            global haderror
            haderror = False
    except KeyboardInterrupt:
        return


def __run(source):
    scanner = Scanner(source, error)
    tokens = scanner.scantokens()
    parser = Parser(tokens, error2)
    statements = parser.parse()

    # Stop if there was a syntax error.
    if haderror:
        return

    interpreter.interpret(statements)


def error(line, message):
    __report(line, '', message)


# I had to move this function up.
# def runtimeerror(error):
#     # todo: Refactor.
#     print(error.args[1] + '\n[line ' +
#           error.args[0].line + ']', file=sys.stderr)
#     global hadruntimeerror
#     hadruntimeerror = True


def __report(line, where, message):
    print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
    global haderror
    haderror = True


# def error
def error2(token, message):
    if token.type == TokenType.EOF:
        __report(token.line, ' at end', message)
    else:
        __report(token.line, ' at \'' + token.lexeme + '\'', message)


if __name__ == '__main__':
    main()
