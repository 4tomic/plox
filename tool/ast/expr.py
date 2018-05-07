class Expr:
    pass
class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

class Literal(Expr):
    def __init__(self, value):
        self.value = value

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


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
    
    def visit_Binary(self, visitor, *args, **kwargs):
        print(visitor.__name__ + 'visit_Binary')

    def visit_Grouping(self, visitor, *args, **kwargs):
        print(visitor.__name__ + 'visit_Grouping')

    def visit_Literal(self, visitor, *args, **kwargs):
        print(visitor.__name__ + 'visit_Literal')

    def visit_Unary(self, visitor, *args, **kwargs):
        print(visitor.__name__ + 'visit_Unary')


