import sys

arg = sys.argv
comand=['']

#Operadores
def asignacion(c):
    if c == '=' or c == '+=' or c == '-=' or c== '*=' or c == '/=':
        return True
    else:
        return False

def logico(c):
    if c == 'and' or c == 'or' or c == 'not' or c== 'is':
        return True
    else:
        return False

def relational(c):
    if c == '==' or c == '<=' or c == '>=' or c== '!=' or c == '<' or c == '>':
        return True
    else:
        return False

def aritmetico(c):
    if c == '+' or c == '-' or c == '*' or c== '/':
        return True
    else:
        return False
    
def esOperador(c):
    if aritmetico(c) or relational(c) or logico(c) or asignacion(c):
        return True
    else:
        return False


#delimitadores
def sinbol(c):
    if c == ';' or c == ',':
        return True
    else:
        return False

def corchetes(c):
    if c == '[' or c == ']':
        return True
    else:
        return False

def llaves(c):
    if c == '{' or c == '}':
        return True
    else:
        return False

def parentesis(c):
    if c == '(' or c == ')':
        return True
    else:
        return False

def esDelimitador(c):
    if parentesis(c) or llaves(c) or corchetes(c) or sinbol(c):
        return True
    else:
        return False

#Comentario
def linea(c):
    if c == '//' or c == '#':
        return True
    else:
        return False

def multiLinea(c):
    if c == '/*' or c == '*/':
        return True
    else:
        return False

def esComentador(c):
    if multiLinea(c) or linea(c):
        return True
    else:
        return False


#Separadores

def esSeparador(c):
    if c == ' ' or c == '\t':
        return True
    else:
        return False

#palabras claves
def keywords(c):
    if c == 'if' or c == 'else' or c == 'for' or c == 'while' or c == 'return':
        return True
    else:
        return False

def numero(c):
    if c.isdigit():
        return True
    else:
        return False

def alfabeto(c):
    if c.isalpha():
        return True
    else:
        return False

def main():
    com = 'profundidad = (9,8 * t^2) / 2'
    if len(arg) > 1:
        if '-oper' in arg:
            i = arg.index('-oper')
            if i < len(arg):
                print(esOperador(arg[i+1]))
            else:
                print('Debe ingresar un valor despues del comando ',arg[i],'\n')
                
        if '-deli' in arg:
            i = arg.index('-deli')
            if i < len(arg):
                print(esOperador(arg[i+1]))
            else:
                print('Debe ingresar un valor despues del comando ',arg[i],'\n')
                
        if '-comen' in arg:
            i = arg.index('-comen')
            if i < len(arg):
                print(esOperador(arg[i+1]))
            else:
                print('Debe ingresar un valor despues del comando ',arg[i],'\n')

        
    else:
        print('Error introduca la cantidad de Argumentos necesarios')
        print('Ejemplo: ', sys.argv[0],"hola mundo", 5)
    
    
if __name__ == '__main__':
    main()