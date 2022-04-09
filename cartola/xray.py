# -*- coding: UTF-8 -*-
#
# Copyright 2015-2022 Flávio Gonçalves Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ast
import inspect
import sys


if (sys.version_info.major, sys.version_info.minor) > (3, 8):
    def class_decorators(target):
        """ Return a dictionary with all decorators for each class found in the
        given target.
        The target could be either a class or a module

        # Won't work on python 3.6 to 3.8. This is good for 3.9 and upwards.

        From https://bit.ly/3v7KLtm
        :param target: A class or module
        :return: An dictionary with all decorators for each class found in
        target
        """
        decorators = {}

        def visit_class_def(node: ast.ClassDef):
            decorators[node.name] = []
            for n in node.decorator_list:
                if isinstance(n, ast.Name):
                    name = n.id
                    decorators[node.name].append(name)
        node_iter = ast.NodeVisitor()
        node_iter.visit_ClassDef = visit_class_def
        node_iter.visit(ast.parse(inspect.getsource(target)))
        return decorators


def methods_decorators(target):
    """ Return a dictionary with all decorators for each method found in the
    given target class.

    From https://bit.ly/3v7KLtm
    :param target: A class
    :return: An dictionary with all decorators for each method from the target
    class
    """
    decorators = {}

    def visit_func_def(node: ast.FunctionDef):
        decorators[node.name] = []
        for n in node.decorator_list:
            if isinstance(n, ast.Name):
                name = n.id
                decorators[node.name].append(name)
    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_func_def
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators
