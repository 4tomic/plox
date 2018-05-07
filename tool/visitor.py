#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://peter-hoffmann.com/2010/extrinsic-visitor-pattern-python-inheritance.html
*TL;DR80
Separates an algorithm from an object structure on which it operates.
"""


class Node(object):
    def hello(self):
        print(self.__class__.__name__,"say hello")


class A(Node):
    pass


class B(Node):
    pass


class C(A, B):
    pass


class Visitor(object):

    def visit(self, node, *args, **kwargs):
        method = None
        for cls in node.__class__.__mro__:
            print(node.__class__.__mro__)
            method_name = 'visit_' + cls.__name__
            method = getattr(self, method_name, None)
            if method:
                break

        if not method:
            method = self.generic_visit
        return method(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print('generic_visit ' + node.__class__.__name__)
        node.hello()

    def visit_B(self, node, *args, **kwargs):
        print('visit_B ' + node.__class__.__name__)
        node.hello()


if __name__ == '__main__':
    a = A()
    b = B()
    c = C()
    visitor = Visitor()
    visitor.visit(a)
    visitor.visit(b)
    visitor.visit(c)

### OUTPUT ###
# generic_visit A
# visit_B B
# visit_B C
