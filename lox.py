import sys
from lox.scanner import Scanner


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

    # For now, just print the tokens.
    for token in tokens:
        print(token)


def error(line, message):
    __report(line, '', message)


def __report(line, where, message):
    print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
    global haderror
    haderror = True


if __name__ == '__main__':
    main()
