# coding: utf-8
from sly import Lexer
import os
import re
TESTS = []

CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                      for i in ['0','1']
                      for j in range(16)]

CARACTERES_CONTROL += [bytes.fromhex(hex(127)[-2:]).decode('ascii')]
class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID, ELSE,CASE,CLASS,ESAC,FI,IF,IN,INHERITS,ISVOID,LET,LOOP,NEW,NOT,OF,POOL,THEN,WHILE,ASSIGN,DARROW,LE,STR_CONST,ERROR}
    literals = { '=', '+', '-', '*', '/', '(', ')', '<', '.',',','~',';',':','(',')', '@', '{','}'}    
    ELSE = r'[eE][lL][sS][eE]'
    CASE =r'[cC][aA][sS][eE]\b'
    CLASS =r'[cC][lL][aA][sS][sS]\b'
    ESAC =r'[eE][sS][aA][cC]\b'
    FI =r'[fF][iI]\b'
    IF =r'[iI][fF]\b'
    INHERITS = r'[iI][nN][hH][eE][rR][iI][tT][sS]'
    IN =r'[iI][nN]\b'
    ISVOID = r'[iI][sS][vV][oO][iI][dD]'
    LET = r'[lL][eE][tT]'
    LOOP = r'[lL][oO][oO][pP]\b'
    NEW = r'[nN][eE][wW]\b'
    NOT = r'[nN][oO][tT]\b'
    OF = r'[oO][fF]\b'
    POOL = r'[pP][oO][oO][lL]\b'
    THEN = r'[tT][hH][eE][nN]\b'
    WHILE = r'[wW][hH][iI][lL][eE]\b'
    ASSIGN = r'<-'
    DARROW = r'=>'
    LE = r'<='
    
    @_(r'"([^"\n\\\x00]|([^\\"]?(\\\\)*\\(\n|[^\x00])))*"')
    def STR_CONST(self,t):
        
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        if '\\\x00' in t.value:
            t.type = 'ERROR'
            t.value = '"String contains escaped null character."'
            return t
        elif '\x00' in t.value:
            t.type = 'ERROR'
            t.value = '"String contains null character."'
            return t
        

        t.value = t.value.replace('\\\n','\\n')
        t.value = t.value.replace('\\\t',r'\t')
        t.value = t.value.replace('\\\b',r'\b')
        t.value = t.value.replace('\\\f',r'\f')
        t.value = t.value.replace('\t',r'\t')
        t.value = t.value.replace('\f',r'\f')
        r = re.compile(r'(?<!\\)\\([^nftb"\\])')
        t.value = r.sub(r'\1', t.value)
        new_value = []
        if len(bytes(str(t.value[1:-1]), "utf-8").decode("unicode_escape")) > 1024:
            t.type = "ERROR"
            t.value = '"String constant too long"'
            return t
        for c in t.value:
            if c in CARACTERES_CONTROL:
                new_value.append(
                    '\\'+str(oct(int(c.encode("ascii").hex(), 16)).replace('o', '0'))[-3:])
            else:
                new_value.append(c)

        t.value = ''.join(new_value)


        return t
    @_(r'[!#$%^&_>\?`\[\]\\\|\x00]')
    def invalidCharacter(self, t):
        t.type = "ERROR"
        if t.value == '\\':
            t.value = '\\\\'
        if t.value in CARACTERES_CONTROL:
            t.value = '\\' + \
                str(oct(int(t.value.encode("ascii").hex(), 16)
                        ).replace('o', '0')[-3:])
        t.value = '"'+t.value+'"'
        return t
    @_(r'||Õ|˜£|')
    def undernormalChars(self,t):
        pass
        
        
  
    @_(r'\(\*')
    def comentario(self,t):
        return self.begin(Comentario)
    @_(r'\*\)')
    def unmatched(self,t):
     t.type = "ERROR"
     t.value = '"Unmatched *)"'
     return t
    @_(r'--.*')
    def comentarioLinea(self, t):
        self.lineno+=t.value.count('\n')
        pass
    @_(r'"([^"\n\x00]*\\\x00[^"\n\x00]*)+"?')
    def escapedNull(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"String contains escaped null character."'
        return t
  
    @_(r'"([^"\n\x00]*\x00[^"\n\x00]*)+"?')
    def nullChar(self,t):
        
        t.type = "ERROR"
        t.value = '"String contains null character."'
        return t
    @_(r'("(?:\\["]|[^"\\\n]|\\[\n\\a-zA-Z\d\x00])*)\n')
    def unterminated (self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"Unterminated string constant"'
        return t
         
   
    
   
    @_(r'\d+')
    def INT_CONST(self, t):
        t.type = "INT_CONST"
        t.value=str(t.value)
        return t
  
    @_(r't[rR][uU][eE]\b|f[aA][lL][sS][eE]\b')
    def BOOL_CONST(self, t):
        if t.value[0] == "t":
            t.value = True
        else:
            t.value = False
        return t
    @_(r'\"([^\"]|\\\")*\Z')
    def EOFstring(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        return t
    
   

    @_(r'[A-Z][a-zA-Z0-9_]*')
    def TYPEID(self, t):
        t.value = str(t.value)
        return t

    @_(r'[a-z_][a-zA-Z0-9_]*')
    def OBJECTID(self, t):
        return t

    @_(r'\t| ')
    def spaces(self, t):
        pass
    

  
       
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
  
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    def salida(self, texto):
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':

                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type == 'INT_CONST':
                result += f"{str(token.value)}"
            elif token.type=='STR_CONST':
                 result += f"{str(token.value)}"
            elif token.type=='ERROR':
                 result += f"{str(token.value)}"
            elif token.type in self.literals:
                 

                 result = f'#{token.lineno} \'{token.type}\' '
            else:

                    result = f'#{token.lineno} {token.type}'
            
            list_strings.append(result)
        if texto.count('(*') > texto.count('*)'):
            list_strings.append(f'#{self.lineno} ERROR "EOF in comment"')

        return list_strings

    def tests(self):
        for fich in TESTS:
            f = open(os.path.join(DIR, fich), 'r')
            g = open(os.path.join(DIR, fich + '.out'), 'r')

            resultado = g.read()
            entrada = f.read()
            texto = '\n'.join(self.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
        

            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")
                


lexer = CoolLexer()
class Comentario(Lexer):
    tokens = {ERROR}
    parentesisAbiertos=1
    
    @_(r'\(\*')
    def nuevoParentesis(self,t):
        self.parentesisAbiertos=self.parentesisAbiertos+1
    @_(r'\*\)')
    def cierraParentesis(self, t):
        self.parentesisAbiertos -= 1
        if self.parentesisAbiertos == 0 :
            self.parentesisAbiertos= 1
            self.begin(CoolLexer)
   
    @_(r'\t| ')
    def spaces(self, t):
        
        pass
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
       
    @_(r'.')
    def contenidoComentario(self,t):
        
            pass
        
    
    

if __name__ == '__main__':
    for fich in TESTS:
        lexer = CoolLexer()
        f = open(os.path.join(DIR, fich), 'r')
        g = open(os.path.join(DIR, fich + '.out'), 'r')
        h = open(os.path.join(DIR, fich + '.try'), 'w')
        resultado = g.read()
        texto = ''
        entrada = f.read()
        texto = '\n'.join(lexer.salida(entrada))
        texto = f'#name "{fich}"\n' + texto
        h.write(texto)
        f.close(), g.close()
        if texto.strip().split() != resultado.strip().split():
            print(f"Revisa el fichero {fich}")
            

        h.close()
  


