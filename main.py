# coding: utf-8

from Clases import *
from Lexer import CoolLexer
from sly import Parser
import sys
import os
DIRECTORIO = os.path.join(r"./")

sys.path.append(DIRECTORIO)

GRADING = os.path.join(DIRECTORIO, 'ficheros')
FICHEROS = os.listdir(GRADING)

TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(GRADING, fich))
         and fich.endswith(".test")]
TESTS = ['missingclass.test'] 
print(TESTS)
class CoolParser(Parser):

    tokens = CoolLexer.tokens
    errores = []
    debugfile = "salida.txt"

    noHeredables = (
      'String', 'Int'
    )


    precedence = (
        ('left', 'IN','LET'),
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', '<','LE','='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID'),
        ('left', '@'),
        ('left', '.'),
        ('right', '~')
    )

########################################################################################################################
                                        #Programa#
########################################################################################################################
    
    @_('lista_clases')
    def programa(self, p):
        return Programa(0, p[0])
    
########################################################################################################################
                                        #Clases#
########################################################################################################################
    
    @_('clase ";"')
    def lista_clases(self, p):
        return [p[0]]
    
    @_('lista_clases clase ";"')
    def lista_clases(self, p):
        return p[0]+[p[1]]
    
    @_('CLASS TYPEID INHERITS TYPEID "{" lista_atributos "}"')
    def clase(self, p):
      return Clase(p.lineno, p[1], p[3], parser.nombre_fichero, p[5])
    
    @_('CLASS TYPEID "{" lista_atributos "}"')
    def clase(self, p):
        return Clase(p.lineno, p[1], 'Object', parser.nombre_fichero, p[3])

  

    
########################################################################################################################
                                        #Atributos#
########################################################################################################################
    
    @_('')
    def lista_atributos(self, p):
        return []
    
    @_('lista_atributos atributo ";"')
    def lista_atributos(self, p):
        return p[0]+[p[1]]
    
    @_('OBJECTID "(" lista_formales ")" ":" TYPEID "{" expresion "}"')
    def atributo(self, p):
        return Metodo(p.lineno, p[0], p[5], p[7], p[2])

    @_('OBJECTID ":" TYPEID')
    def atributo(self, p):
        return Atributo(p.lineno, p[0], p[2], NoExpr(p.lineno))

    @_('OBJECTID ":" TYPEID ASSIGN expresion')
    def atributo(self, p):
        return Atributo(p.lineno, p[0], p[2], p[4])
    
########################################################################################################################
                                            #Formal#
########################################################################################################################
    
    @_('')
    def lista_formales(self,p) :
        return []

    @_('formal')
    def lista_formales(self,p) :
        return [p[0]]
    
    @_('formal "," lista_formales')
    def lista_formales(self, p):
        return [p[0]] + p[2]
    
    @_('OBJECTID ":" TYPEID')
    def formal(self, p):
        return Formal(p.lineno, p[0], p[2])
    
########################################################################################################################
                                        #Expresiones#
########################################################################################################################
    
    @_('expresion ";"')
    def lista_expresiones(self, p):
        return [p[0]]

    @_('expresion ";" lista_expresiones')
    def lista_expresiones(self, p):
        return [p[0]] + p[2]

    @_('lista_argumentos')
    def expr_enumeration(self, p):
        return p[0]

    @_('')
    def expr_enumeration(self, p):
        return []
    
    @_('expresion')
    def lista_argumentos(self,p) :
        return [p[0]]
    
    @_('lista_argumentos "," expresion')
    def lista_argumentos(self, p):
        return p[0] + [p[2]]
    
    @_('OBJECTID ASSIGN expresion')
    def expresion(self, p):
        return Asignacion(p.lineno, p[0], p[2])
    
    @_('expresion "@" TYPEID "." OBJECTID "(" expr_enumeration ")"')
    def expresion(self, p):
        return LlamadaMetodoEstatico(p.lineno, p[0], p[2], p[4], p[6])
    
    @_('expresion "." OBJECTID "(" expr_enumeration ")"')
    def expresion(self, p):
        return LlamadaMetodo(p.lineno, p[0], p[2], p[4])
    
    @_('OBJECTID "(" expr_enumeration ")"')
    def expresion(self, p):
        return LlamadaMetodo(p.lineno, Objeto(p.lineno,"self"), p[0], p[2])
    
    @_('IF expresion THEN expresion ELSE expresion FI')
    def expresion(self, p):
        return Condicional(p.lineno, p[1], p[3], p[5])
    
    @_('WHILE expresion LOOP expresion POOL')
    def expresion(self, p):
        return Bucle(p.lineno, p[1], p[3])
    
    @_('"{" lista_expresiones "}"')
    def expresion(self, p):
        return Bloque(p.lineno, p[1])
    
    @_('LET OBJECTID ":" TYPEID ASSIGN expresion lista_id IN expresion')
    def expresion(self, p):
        p[6].insert(0,(p[1], p[3],p[5]))
        lista = p[8]
        for nombre, tipo, inicializacion in reversed(p[6]):
            lista = Let(p.lineno, nombre, tipo, inicializacion, lista)
        return lista

    @_('LET OBJECTID ":" TYPEID ASSIGN error lista_id IN expresion')
    def expresion(self, p):
        return [Nodo(p.lineno)]
    
    @_('LET OBJECTID ":" TYPEID lista_id IN expresion')
    def expresion(self, p):
        p[4].insert(0,(p[1], p[3], NoExpr(p.lineno)))
        lista = p[6]
        for nombre, tipo, inicializacion in reversed(p[4]):
            lista = Let(p.lineno, nombre, tipo, inicializacion, lista)
        return lista
    
    @_('LET OBJECTID ":" TYPEID ASSIGN expresion IN expresion')
    def expresion(self, p):
        return Let(p.lineno, p[1], p[3], p[5], p[7])

    @_('LET OBJECTID ":" TYPEID IN expresion')
    def expresion(self, p):
        return Let(p.lineno, p[1], p[3], NoExpr(p.lineno), p[5])
    
    @_('"," OBJECTID ":" TYPEID ASSIGN expresion')
    def lista_id(self, p):
        return [(p[1], p[3], p[5])]
    
    @_('"," OBJECTID ":" TYPEID')
    def lista_id(self, p):
        return [(p[1], p[3], NoExpr(p.lineno))]

    @_('lista_id "," OBJECTID ":" TYPEID ASSIGN expresion')
    def lista_id(self, p):
        return p[0] + [(p[2], p[4], p[6])]

    @_('lista_id "," OBJECTID ":" TYPEID')
    def lista_id(self, p):
        return p[0] + [(p[2], p[4], NoExpr(p.lineno))]
    
    @_('"," OBJECTID ":" error ASSIGN expresion')
    def lista_id(self, p):
        return [Nodo(p.lineno)]
    
    @_('"," OBJECTID ":" error')
    def lista_id(self, p):
        return [Nodo(p.lineno)]

    @_('lista_id "," OBJECTID ":" error ASSIGN expresion')
    def lista_id(self, p):
        return [Nodo(p.lineno)]

    @_('lista_id "," OBJECTID ":" error')
    def lista_id(self, p):
        return [Nodo(p.lineno)]    

    @_('OBJECTID ":" TYPEID DARROW expresion ";"')
    def case(self, p):
        return RamaCase(p.lineno,p[0],p[2],p[4])
    
    @_('CASE expresion OF lista_cases ESAC')
    def expresion(self, p):
        return Swicht(p.lineno,p[1],p[3])
    
    @_('case')
    def lista_cases(self, p):
        return [p[0]]
    
    @_('lista_cases case')
    def lista_cases(self, p):
        return p[0] + [p[1]]
    
    @_('NEW TYPEID')
    def expresion(self, p):
        return Nueva(p.lineno, p[1])
    
    @_('ISVOID expresion')
    def expresion(self, p):
        return EsNulo(p.lineno, p[1])
    
    @_('expresion "+" expresion')
    def expresion(self, p):
        return Suma(p.lineno, p[0], p[2])
    
    @_('expresion "-" expresion')
    def expresion(self, p):
        return Resta(p.lineno, p[0], p[2])
    
    @_('expresion "*" expresion')
    def expresion(self, p):
        return Multiplicacion(p.lineno, p[0], p[2])
    
    @_('expresion "/" expresion')
    def expresion(self, p):
        return Division(p.lineno, p[0], p[2])
    
    @_('"~" expresion')
    def expresion(self, p):
        return Neg(p.lineno, p[1])
    
    '''@_('expresion "<" expresion')
    def expresion(self, p):
        return Menor(p.lineno, p[0], p[2])
    
    @_('expresion LE expresion')
    def expresion(self, p):
        return LeIgual(p.lineno, p[0], p[2])'''
    
    @_('expresion "=" expresion')
    def expresion(self, p):
        return Igual(p.lineno,p[0], p[2])
    
    @_('NOT expresion')
    def expresion(self, p):
        return Not(p.lineno, p[1])
    
    @_('"(" expresion ")"')
    def expresion(self, p):
        return p[1]
    
    @_('OBJECTID')
    def expresion(self, p):
        return Objeto(p.lineno,'' ,p[0])
    
    @_('INT_CONST')
    def expresion(self, p):
        return Entero(p.lineno,'' ,p[0])
    
    @_('STR_CONST')
    def expresion(self, p):
        return String(p.lineno,'', p[0])
    
    @_('BOOL_CONST')
    def expresion(self, p):
        return Booleano(p.lineno,'', p[0])

    @_('expresion LE expresion')
    def expresion(self, p):
        return LeIgual(p.lineno,p[0],p[2])

    @_('expresion "<" expresion')
    def expresion(self, p):
        return Menor(p.lineno,p[0],p[2])
    
########################################################################################################################
                                                #Errores#
########################################################################################################################
    
    @_('"{" error ";" lista_expresiones "}"')
    def expresion(self, p):
        return [Nodo(p.lineno)]

    @_('error ";"')
    def lista_atributos(self, p):
        return []

    @_('error ";" formal')
    def lista_formales(self,p):
        return [Nodo(p.lineno)]
    
    @_('OBJECTID "(" lista_formales ")" ":" TYPEID "{" error "}"')
    def atributo(self, p):
        return Nodo(p.lineno)


    def error(self, p):
        print('error', p)
        if p!= None:
            temp = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near '
            if p.type in {'IF', 'FI','OF', 'ELSE', 'POOL', 'LOOP', 'LE', 'ESAC', 'DARROW'}:
                temp += f'{p.type}'
            elif p.type in CoolLexer.tokens:
                temp += f'{p.type} = {p.value}'
            elif p.type in CoolLexer.literals:
                temp += f"'{p.type}'"
        else:
            temp = '"emptyprogram.test", line 0: syntax error at or near EOF'
        self.errores.append(temp)
        print(temp)

    
        



########################################################################################################################
                                                #Lectura ficheros#
########################################################################################################################

for i, fich in enumerate(TESTS):
    f = open(os.path.join(GRADING, fich), 'r')
    g = open(os.path.join(GRADING, fich + '.out'), 'r')
    h = open(os.path.join(GRADING, fich + '.try'), 'w')
    print('')
    print(f"Fichero {fich}", i+1)
    
    lexer = CoolLexer()
    lexer1 = CoolLexer()
    parser = CoolParser()
    parser.errores = []

    parser.nombre_fichero = fich
    bien = ''.join([c for c in g.readlines() if c and '#' not in c])
    entrada = f.read()
    j = parser.parse(lexer.tokenize(entrada))
    parser.errores += j.analizaPrograma()
    
    for t0 in lexer1.tokenize(entrada):
        pass
    if j and not parser.errores:
        resultado = '\n'.join([c for c in j.str(0).split('\n')
                               if c and '#' not in c])
    else:
       for i in range(len(parser.errores)):
        parser.errores[i]=fich+": "+parser.errores[i]
        resultado = '\n'.join(parser.errores)
        resultado += '\n' + "Compilation halted due to lex and parse errors."
        
    #h.write(resultado)
    f.close(), g.close()

    bien = bien.strip()
    h.write(resultado)
    h.close()
    if resultado != bien:
        print(f"Revisa el fichero {fich}")
