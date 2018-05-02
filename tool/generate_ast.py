from utils import log

import sys

_class_template = """\
class {base_name}:
    pass
"""

_inner_class = """\
class {class_name}({base_name}):
    def __init__(self, {property}):
{init}
"""


class GenerateAST:
    def __init__(self):
        pass

    def meta(self, base_name):
        class_definition = _class_template.format(
            base_name=base_name,
        )
        namespace = dict(__name__='{0}'.format(base_name))
        log(namespace)
        exec(class_definition, namespace)
        result = namespace[base_name]
        result._source = class_definition
        log(result._source)

    def define_ast(self, output, base_name, types):
        class_definition = _class_template.format(
            base_name=base_name,
        )

        inner_class = ''
        for class_name, fields in types.items():
            # log(class_name, ':', fields)
            inner_class += self.define_type(base_name, class_name, fields)

        # namespace = dict(__name__='namedtuple_{0}'.format(base_name))
        # log(namespace)
        # exec(class_definition, namespace)
        # result = namespace[base_name]
        # result._source = class_definition
        # log(result._source)

        path = output + '/' + base_name.lower() + '.py'
        log(path)
        # with open(path, 'w') as f:
        #     f.write(class_definition + inner_class)
        f = open(path, 'w')
        f.write(class_definition + inner_class)
        f.close()

    @staticmethod
    def define_type(base_name, class_name, fields):
        # log('define_type: ', fields)
        field_list = fields.split(', ')
        # log('field_list', field_list)
        properties = []
        init = ''
        four_blank = '    '
        for field in field_list:
            name = field.split(' ')[1]
            properties.append(name)
            init += four_blank * 2 + 'self.' + name + ' = ' + name + '\n'

        class_definition = _inner_class.format(
            class_name=class_name,
            base_name=base_name,
            property=', '.join(properties),
            init=init,
        )

        return class_definition


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: generate_ast <output directory>')
        sys.exit(1)
    output_dir = sys.argv[1]
    log(output_dir)

    ast = GenerateAST()
    ast.define_ast(output_dir, "Expr", {
        'Binary': 'Expr left, Token operator, Expr right',
        'Grouping': 'Expr expression',
        'Literal': 'Object value',
        'Unary': 'Token operator, Expr right',
    })
