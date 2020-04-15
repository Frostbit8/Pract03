# coding: utf-8
from dataclasses import dataclass, field
from typing import List

class TablaSimbolos:
  l = []
  simbolos=dict()
  metodos=dict()
  def NuevoAmbito(self):
    self.l.append(dict())
  def SalirAmbito(self):
    self.l.pop()
  

@dataclass
class Nodo:
    linea: int
    def str(self, n):
        return f'{n*" "}#{self.linea}\n'


ambito_programa = TablaSimbolos()

class nodoArbol:
  def __init__(self, nombre):
    self.nombre=nombre
    self.metodos=dict()
  



class Arbol(object):
      def __init__(self, padre, elemento):
        self.hijos = []
        self.raiz = elemento
        self.padre= padre
      def agregarHijo (self,  elementoPadre,elemento):    
        subarbol = self.buscarSubarbol(elementoPadre)
        subarbol.hijos.append(Arbol(elementoPadre,elemento))

      def buscarSubarbol(self, elemento):
        if self.raiz.nombre == elemento.nombre:
            return self
        for subarbol in self.hijos:
            arbolBuscado = subarbol.buscarSubarbol(elemento)
            if (arbolBuscado != None):
                return arbolBuscado
        return None   
      
      def anhadeMetodo(self,elemento,nombre,formales,tipo):
          self.buscarSubarbol(elemento).raiz.metodos[nombre]=(formales,tipo)



@dataclass
class Formal(Nodo):
    nombre_variable: str
    tipo: str
    def analiza():
        self.cast = self.tipo
        return []

    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado

@dataclass
class Expresion(Nodo):
    cast: str

    


@dataclass
class Asignacion(Expresion):
    nombre: str
    cuerpo: Expresion
    def analiza(self):
       
        Error = []
        Error += self.cuerpo.analiza()
       
        if self.nombre in ambito:
            if self.nombre == 'self':
              self.cast = ambito["SELF_TYPE"]
              Error += ["Cannot assign to 'self'."]
              return Error
            cast_nombre = ambito[self.nombre]
            
        else:
            cast_nombre = 'Object'
            Error += ["Error 25"]
        
        
        return Error


    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion
    clase: str
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Condicional(Expresion):
    condicion: Expresion
    verdadero: Expresion
    falso: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Bucle(Expresion):
    condicion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Let(Expresion):
    nombre: str
    tipo: str
    inicializacion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado


@dataclass
class RamaCase(Nodo):
    nombre_variable: str
    tipo: str
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado


@dataclass
class Swicht(Nodo):
    expr: Expresion
    casos: List[RamaCase]
    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class Nueva(Nodo):
    tipo: str
    def analiza(self):
      self.cast=self.tipo
      return ''   
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion
    derecha: Expresion
    def analiza(self):
      error=self.izquierda.analiza()
      error=error+self.derecha.analiza()
      if self.izquierda.cast=='INT' and self.derecha.cast=='INT':
        self.cast='INT'
      else:
        return error+'ERROR'

@dataclass
class OperacionBinariaBoolean(Expresion):
    izquierda: Expresion
    derecha: Expresion
    def analiza(self):
      if self.izquierda.cast=='BOOLEAN' and self.derecha.cast=='BOOLEAN':
        self.cast='BOOLEAN'
      else:
        return "ERROR"


@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'
    

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Menor(OperacionBinariaBoolean):
    operando: str = '<'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
@dataclass
class LeIgual(OperacionBinariaBoolean):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Igual(OperacionBinariaBoolean):
    operando: str = '='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class Neg(OperacionBinariaBoolean):
    expr: Expresion
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class Not(OperacionBinariaBoolean):
    expr: Expresion
    operador: str = 'NOT'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class EsNulo(OperacionBinariaBoolean):
    expr: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado




@dataclass
class Objeto(Expresion):
    nombre: str

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
        
    def analiza(self):
        Error = []
        if self.nombre in ambito:
            self.cast = ambito[self.nombre]
        else:
            self.cast = "Object"
            Error+=[f"Undeclared identifier {self.nombre}."]
        return Error





@dataclass
class NoExpr(Expresion):
    nombre: str = ''
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Entero(Expresion):
    valor: int
    
    def analiza(self):
      self.cast='Int'
      return''
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class String(Expresion):
    valor: str
    def analiza(self):
      self.cast='str'
      return ''
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class Booleano(Expresion):
    valor: bool
    def analiza(self):
      self.cast='bool'
      return ''
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def analiza(self):
        self.cast = "Bool"
        return []

@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado

    def analizaPrograma(self):
      clases=[]
      for secuencia in self.secuencia:
            if secuencia.nombre == "Main":
                main = True
            if secuencia.nombre in clases:
                error += [f"Class {secuencia.nombre} was previously defined."]
            else:
                clases.append(secuencia.nombre)
            
      if not main:
            return [f"Class Main is not defined."]

      classTree=Arbol(nodoArbol(None),nodoArbol('Object'))
      classTree.agregarHijo(nodoArbol('Object'),nodoArbol('Bool'))
      classTree.agregarHijo(nodoArbol('Object'),nodoArbol('String'))
      classTree.agregarHijo(nodoArbol('Object'),nodoArbol('IO'))

      classTree.anhadeMetodo(nodoArbol('Object'),"abort",[],'Object')
      classTree.anhadeMetodo(nodoArbol('Object'),"type_name",[],'String')
      classTree.anhadeMetodo(nodoArbol('Object'),"copy",[],'SELF_TYPE')
      classTree.anhadeMetodo(nodoArbol('IO'),'out_string',[Formal(0,'out_string','String')],'SELF_TYPE')
      classTree.anhadeMetodo(nodoArbol('IO'),'out_int',[Formal(0,'out_int','Int')],'SELF_TYPE')
      classTree.anhadeMetodo(nodoArbol('IO'),'in_string',[],'String')
      classTree.anhadeMetodo(nodoArbol('IO'),'in_int',[],'Int')

      classTree.anhadeMetodo(nodoArbol('String'),'length',[],'Int')
      classTree.anhadeMetodo(nodoArbol('String'),'concat',[Formal(0,'concat','String')],'String')
      classTree.anhadeMetodo(nodoArbol('String'),'substr',[Formal(0,'substr','Int'), Formal(0,'substr','Int')],'"String"')



      
      Error = []

      for clase in self.secuencia:
            
            Error+= clase.analiza(classTree)
        
      print(Error)
        
      return Error

@dataclass
class Caracteristica(Nodo):
    nombre: str
    tipo: str
    cuerpo: Expresion
    

@dataclass
class Clase(Nodo):
    nombre: str
    padre: str
    nombre_fichero: str
    caracteristicas: List[Caracteristica] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado
    def analiza(self,classTree):
      Error = []

      global ambito_programa
      ambito_programa.NuevoAmbito()
      if  classTree.buscarSubarbol(nodoArbol(self.padre)) == None:
            Error +=[f"Class {self.nombre} inherits from an undefined class {self.padre}."]
            return Error
      if self.padre == "SELF_TYPE":
            Error += [f"Class {self.nombre} cannot inherit class SELF_TYPE."]
            return Error
      #####
      
      ##### Guardar en diccionario nuevo y añadir a la tabla de símbolos

      #####
      for c in self.caracteristicas:
        c.analiza()
        '''
        if type(c)==Atributo:
          ambito_programa.añade_simbolo(c.nombre, c.tipo, c.cuerpo)
        else:
          ambito_programa.añade_metodo(c.nombre, c.tipo, c.cuerpo,c.formales)
        '''
      #####
      ambito_programa.SalirAmbito()
      return Error


@dataclass
class Metodo(Caracteristica):
    formales: List[Formal]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def analiza(self):
      global ambito_programa
      nuevo_ambito=ambito_programa.NuevoAmbito()
      Definidos=[]
      Error = []
      for formal in self.formales: 
        if formal.nombre_variable in Definidos:
                Error += [f"Formal parameter {e.nombre_variable} is multiply defined."]
        else:
                aux.append(e.nombre_variable)
        if formal.nombre_variable == "self":
                Error += [f"'self' cannot be the name of a formal parameter."]
        if formal.tipo == "SELF_TYPE":
                Error += [f"Formal parameter {e.nombre_variable} cannot have type SELF_TYPE."]
        nuevo_ambito[formal.nombre_variable] = formal.tipo
       Error += self.cuerpo.analiza()
      ambito_programa.SalirAmbito()
      return "" + error

class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def analiza(self):
        Error = []
        if self.nombre == "self":
            Error += ["'self' cannot be the name of an attribute."]
        
        Error +=  self.cuerpo.analiza()
 
        return Error
