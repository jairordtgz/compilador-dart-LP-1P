import ply.lex as lex
import os
from datetime import datetime

reserved = {
    'var':      'VAR',
    'int':      'INT',
    'double':   'DOUBLE',
    'String':   'STRING_TYPE',
    'bool':     'BOOL',
    'dynamic':  'DYNAMIC',
    'final':    'FINAL',
    'const':    'CONST',
    'void':     'VOID',
    'return':   'RETURN',
    'if':       'IF',
    'else':     'ELSE',
    'while':    'WHILE',
    'for':      'FOR',
    'in':       'IN',
    'break':    'BREAK',
    'continue': 'CONTINUE',
    'print':    'PRINT',
    'null':     'NULL',
    'true':     'TRUE',
    'false':    'FALSE',
    'import':   'IMPORT',
    'List':     'LIST_TYPE',
    'Map':      'MAP_TYPE',
    'Set':      'SET_TYPE',
}

tokens = (
    'ENTERO', 
    'FLOTANTE', 
    'CADENA', 
    'IDENTIFICADOR',
    'IGUAL_IGUAL', 
    'DIFERENTE',
    'MENOR', 
    'MAYOR', 
    'MENOR_IGUAL', 
    'MAYOR_IGUAL',
    'ASIGNACION',
    'MAS_IGUAL', 
    'MENOS_IGUAL', 
    'PRODUCTO_IGUAL', 
    'DIVISION_IGUAL',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'PAREN_IZQ',
    'PAREN_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'PUNTO_COMA',
    'COMA',
    'PUNTO',
    'DOS_PUNTOS',
    'MODULO',
    'MAS',
    'MENOS',
    'PRODUCTO',
    'DIVISION',
    'DIVISION_ENTERA',
    'AND',
    'OR',
    'NOT',
    'INTERROGACION',
    'COMENTARIO_BLOQUE',
    'COMENTARIO_LINEA'

) + tuple(reserved.values())

#<Carlos Lopez>
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t
#</Carlos Lopez>

#INICIO APORTE JAIRO RODRIGUEZ 

def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'(\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\')'
    t.value = t.value[1:-1]
    return t

t_IGUAL_IGUAL    = r'=='
t_DIFERENTE      = r'!='
t_MENOR_IGUAL    = r'<='
t_MAYOR_IGUAL    = r'>='
t_MENOR          = r'<'
t_MAYOR          = r'>'

t_MAS_IGUAL      = r'\+='
t_MENOS_IGUAL    = r'-='
t_PRODUCTO_IGUAL = r'\*='
t_DIVISION_IGUAL = r'/='
t_ASIGNACION     = r'='
#FIN APORTE JAIRO RODRIGUEZ

#INICIO APORTE CARLOS LÓPEZ

t_LLAVE_IZQ      = r'\{'
t_LLAVE_DER      = r'\}'
t_PAREN_IZQ      = r'\('
t_PAREN_DER      = r'\)'
t_CORCHETE_IZQ   = r'\['
t_CORCHETE_DER   = r'\]'
t_PUNTO_COMA     = r';'
t_COMA           = r','
t_PUNTO          = r'\.'
t_DOS_PUNTOS     = r':'
t_MODULO         = r'%'

def t_COMENTARIO_BLOQUE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMENTARIO_LINEA(t):
    r'//[^\n]*'
    return t

#FIN APORTE CARLOS LÓPEZ

#Inicio de Aporte Benjamin Cedeño

t_MAS = r'\+'
t_MENOS = r'-'
t_PRODUCTO = r'\*'
t_DIVISION = r'/'
t_DIVISION_ENTERA = r'~/'

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_ignore = ' \t\r'

t_INTERROGACION = r'\?'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    msg = (f"[Error Léxico] Línea {t.lexer.lineno}: "
           f"Carácter no reconocido '{t.value[0]}'")
    print(msg)
    if not hasattr(t.lexer, 'errores'):
        t.lexer.errores = []
    t.lexer.errores.append(msg)
    t.lexer.skip(1)



# ============================================================
# LOG Y FUNCIÓN PRINCIPAL
# ============================================================

def generar_log(tokens_encontrados, errores, desarrollador, algoritmo):
    ahora      = datetime.now()
    fecha_hora = ahora.strftime('%d-%m-%Y-%Hh%M')
    nombre_log = f'lexico-{desarrollador}-{fecha_hora}.txt'

    carpeta = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre_log)

    with open(ruta, 'w', encoding='utf-8') as f:
        sep = '=' * 64
        f.write(sep + '\n')
        f.write('  ANÁLISIS LÉXICO — Dart Analyzer\n')
        f.write(f'  Desarrollador : {desarrollador}\n')
        f.write(f'  Algoritmo     : {algoritmo}\n')
        f.write(f'  Fecha/Hora    : {ahora.strftime("%d/%m/%Y %H:%M:%S")}\n')
        f.write(sep + '\n\n')
        f.write(f'TOKENS RECONOCIDOS ({len(tokens_encontrados)}):\n')
        f.write(f"{'Línea':<8}{'Tipo':<24}{'Valor'}\n")
        f.write('-' * 64 + '\n')
        for tok in tokens_encontrados:
            f.write(f"{tok['linea']:<8}{tok['tipo']:<24}{tok['valor']}\n")
        f.write('\n')
        if errores:
            f.write(f'ERRORES ENCONTRADOS ({len(errores)}):\n')
            f.write('-' * 64 + '\n')
            for err in errores:
                f.write(err + '\n')
        else:
            f.write('ERRORES: Ninguno\n')
        f.write('\n' + sep + '\n')

    print(f'\n[Log generado] → logs/{nombre_log}')
    return ruta


def analizar(codigo, desarrollador, algoritmo):
    lexer = lex.lex(debug=False)
    lexer.errores = []
    lexer.input(codigo)

    tokens_encontrados = []
    print(f'\n{"Línea":<8}{"Tipo":<24}{"Valor"}')
    print('-' * 52)

    while True:
        tok = lexer.token()
        if not tok:
            break
        entry = {
            'linea': tok.lineno,
            'tipo':  tok.type,
            'valor': str(tok.value)
        }
        tokens_encontrados.append(entry)
        print(f"{tok.lineno:<8}{tok.type:<24}{tok.value}")

    print(f'\nTotal tokens  : {len(tokens_encontrados)}')
    print(f'Total errores : {len(lexer.errores)}')
    generar_log(tokens_encontrados, lexer.errores, desarrollador, algoritmo)
    return tokens_encontrados, lexer.errores

#Fin de Aporte Benjamin Cedeño