from scanner import Scanner
from parser import Parser
from settings import *
from interpeter import Interpreter

file_path = "/Users/johncabrahams/Desktop/Projects/Research Project/python_compiler/fib.wat"

with open(file_path, 'r', encoding='utf-8') as file:
    text_content=file.read()

tokens = Scanner().scanTokens(text_content)

# Our abstract syntax tree
ast = Parser().parse(tokens)

# Input function name to evaluate
funcName = "fib"
argOne = 1
argTwo = 2
interpreter = Interpreter()
interpreter.instantiate(ast)
print(interpreter.callExtern(funcName, FUNC, 100))

