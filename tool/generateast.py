import sys


def main(args):
    if len(args) != 2:
        print('Usage: generate_ast <output directory>', file=sys.stderr)
        sys.exit(64)
    outputdir = args[1]
    defineast(outputdir, 'Expr', [
        'Binary   : left, operator, right',
        'Grouping : expression',
        'Literal  : value',
        'Unary    : operator, right'
    ])


def defineast(outputdir, basename, types):
    path = outputdir + '/' + basename.lower() + '.py'

    with open(path, 'w', encoding='utf-8') as f:
        f.write('from abc import ABC, abstractmethod\n')
        f.write('\n')
        f.write('\n')
        f.write(f'class {basename}(ABC):\n')
        f.write('    @abstractmethod\n')
        f.write('    def accept(self, visitor): pass\n')

        definevisitor(f, basename, types)

        # The AST classes.
        for type in types:
            classname = type.split(':')[0].strip()
            fields = type.split(':')[1].strip()
            definetype(f, basename, classname, fields)


def definevisitor(f, basename, types):
    # todo: Add a comment for my change.
    f.write('\n')
    f.write('\n')

    f.write('class Visitor(ABC):\n')

    for type in types:
        typename = type.split(':')[0].strip()
        f.write('    @abstractmethod\n')
        f.write(f'    def visit{typename.lower()}{
                basename.lower()}(self, {basename.lower()}): pass\n')


def definetype(f, basename, classname, fieldlist):
    # todo: Add a comment for my change.
    f.write('\n\n')

    f.write(f'class {classname}({basename}):\n')

    # Constructor.
    f.write(f'    def __init__(self, {fieldlist}):\n')

    # Store parameters in fields.
    fields = fieldlist.split(', ')
    for field in fields:
        f.write(f'        self.{field} = {field}\n')

    # Visitor pattern.
    f.write('\n')  # Added by me.
    f.write(f'    def accept(self, visitor):\n')
    f.write(f'        return visitor.visit{
            classname.lower()}{basename.lower()}(self)\n')


if __name__ == '__main__':
    main(sys.argv)
