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

_visitor_template = """\

class Visitor(object):
    def visit(self, visitor_cls, *args, **kwargs):
        method = None
        for cls in visitor_cls.__class__.__mro__:
            print(visitor_cls.__class__.__mro__)
            method_name = 'visit_' + cls.__name__
            method = getattr(self, method_name, None)
            if method:
                break
        if not method:
            method = self.hello

        return method(visitor_cls, *args, **kwargs)
    
    def hello(self, visitor, *args, **kwargs):
        print('Visitor.hello() says hello call by ' + visitor.__name__)
    
{visit_func}
"""

_visit_func = """\
def visit_{derived}(self, visitor, *args, **kwargs):
    print(visitor.__name__ + ' visit_{derived}')
"""


class GenerateAST:
    def __init__(self):
        pass

    # using exec to construct code
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

    # pure string manipulate construction
    # generate AST classes
    def define_ast(self, output, base_name, types):
        class_definition = _class_template.format(
            base_name=base_name,
        )

        # define expression classes
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

        # define visitor
        visitor_class = ''
        class_names = types.keys()
        visitor_class += self.define_visitor(class_names)

        path = output + '/' + base_name.lower() + '.py'
        log(path)
        # with open(path, 'w') as f:
        #     f.write(class_definition + inner_class)
        f = open(path, 'w')
        f.write(class_definition + inner_class + visitor_class)
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

    def define_visitor(self, class_names):
        visit_func = ''
        four_blank = '    '
        str1 = 'def visit_{derived}(self, visitor, *args, **kwargs):\n'
        str2 = "print(visitor.__name__ + 'visit_{derived}')\n\n"
        for class_name in class_names:
            visit_func += four_blank + str1.format(derived=class_name) \
                          + four_blank * 2 + str2.format(derived=class_name)

        class_definition = _visitor_template.format(
            visit_func=visit_func
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
