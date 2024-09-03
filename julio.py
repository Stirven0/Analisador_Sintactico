import sys

arg = sys.argv
comand=['']

#Operadores
def asignacion(c):
    if c == '=' or c == '+=' or c == '-=' or c== '*=' or c == '/=':
        return True
    else:
        return False