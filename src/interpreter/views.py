import sys, os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

from .core.lexer.lexer import Lexer
from .core.parser.parser import Parser
from .core.interpreter import Interpreter, ExceptionType

class InterpreterView(View):

    def get(self, request, *args, **kwargs):
        template_name = "interpreter/interpreter.html"
        return render(request, template_name, {})
        # return HttpResponse(self.template_name)

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        
        path = os.path.normpath("interpreter\\core\\temp\\")
        path_result = os.path.join(path, 'result.txt')
        path_error = os.path.join(path, 'errors.txt')
        stdout = sys.stdout
        sys.stdout = open(path_result, 'w')
        sys.stderr = open(path_error, 'w')

        code = request.POST["code"]
        lexer = Lexer(code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        try:
            interpreter.interpret()
        except ExceptionType as ex:
            print(ex.message)

        sys.stdout = stdout
        result = open(path_result, 'r').read()
        # print(result)

        return_dict = dict()
        return_dict["result"] = result

        return JsonResponse(return_dict)
