import sys
from lox.astprinter import AstPrinter
from lox.parser import Parser
from lox.scanner import Scanner
from lox.tokentype import TokenType


haderror = False


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
    expression = parser.parse()

    # Stop if there was a syntax error.
    if haderror:
        return

    print(AstPrinter().print(expression))


def error(line, message):
    __report(line, '', message)


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
