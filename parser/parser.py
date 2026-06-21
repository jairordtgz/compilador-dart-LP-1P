import ply.yacc as yacc
import ply.lex as lex
from lexer import lexer as lexer_module
from lexer.lexer import tokens
from datetime import datetime
import os

#inicio aporte jairo
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'PRODUCTO', 'DIVISION')
)

def p_programa(p):
    '''
    programa : sentencias
    '''
    
def p_sentencias(p):
    '''
    sentencias : sentencias sentencia
               | sentencia
    '''

def p_declarar_variable(p):
    '''
    sentencia : INT IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | DOUBLE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | STRING_TYPE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | BOOL IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | VAR IDENTIFICADOR ASIGNACION valor PUNTO_COMA
    '''
    
def p_declarar_constante(p):
    '''
    sentencia : FINAL INT IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | FINAL DOUBLE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | FINAL STRING_TYPE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | FINAL BOOL IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | CONST INT IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | CONST DOUBLE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | CONST STRING_TYPE IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | CONST BOOL IDENTIFICADOR ASIGNACION valor PUNTO_COMA
    '''
    
def p_reasignacion(p):
    '''
    sentencia : IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | IDENTIFICADOR MAS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR MENOS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR PRODUCTO_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR DIVISION_IGUAL valor PUNTO_COMA
    '''

def p_valor(p):
    '''
    valor : expresion
          | condicion
          | CADENA
          | TRUE
          | FALSE
    '''
    
def p_expresion_parentesis(p):
    '''
    expresion : PAREN_IZQ expresion PAREN_DER
    '''
    
def p_operacion_matematica(p):
    '''
    expresion : expresion MAS expresion
              | expresion MENOS expresion
              | expresion PRODUCTO expresion
              | expresion DIVISION expresion
    '''

def p_expresion_valor(p):
    '''
    expresion : ENTERO
              | FLOTANTE
              | IDENTIFICADOR
    '''

def p_condicion_relacional(p):
    '''
    condicion : expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion MAYOR_IGUAL expresion
              | expresion MENOR_IGUAL expresion
              | expresion IGUAL_IGUAL expresion
              | expresion DIFERENTE expresion
    '''

def p_condicion_logica(p):
    '''
    condicion : condicion AND condicion
              | condicion OR condicion
    '''

def p_condicion_negada(p):
    '''
    condicion : NOT condicion
    '''

def p_declarar_ed_lista(p):
    '''
    sentencia : LIST_TYPE MENOR INT MAYOR IDENTIFICADOR ASIGNACION lista PUNTO_COMA
              | LIST_TYPE MENOR DOUBLE MAYOR IDENTIFICADOR ASIGNACION lista PUNTO_COMA
              | LIST_TYPE MENOR STRING_TYPE MAYOR IDENTIFICADOR ASIGNACION lista PUNTO_COMA
    '''

def p_lista(p):
    '''
    lista : CORCHETE_IZQ elementos_lista CORCHETE_DER
          | CORCHETE_IZQ CORCHETE_DER
    '''

def p_elementos_lista(p):
    '''
    elementos_lista : elementos_lista COMA valor
                    | valor
    '''
    
def p_funcion_int(p):
    '''
    sentencia : INT IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
              | INT IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
    '''

def p_funcion_double(p):
    '''
    sentencia : DOUBLE IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
              | DOUBLE IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
    '''
    
def p_parametros(p):
    '''
    parametros : parametros COMA parametro
               | parametro
    '''

def p_parametro(p):
    '''
    parametro : INT IDENTIFICADOR
              | DOUBLE IDENTIFICADOR
              | STRING_TYPE IDENTIFICADOR
    '''

def p_llamada_funcion(p):
    '''
    expresion : IDENTIFICADOR PAREN_IZQ argumentos PAREN_DER
              | IDENTIFICADOR PAREN_IZQ PAREN_DER
    '''
    
def p_argumentos(p):
    '''
    argumentos : argumentos COMA valor
               | valor
    '''

def p_if(p):
    '''
    sentencia : IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
    '''


errores_sintacticos = []

def p_error(p):

    if p:
        mensaje = (
            f"Error sintáctico en línea {p.lineno}: "
            f"token inesperado '{p.value}'"
        )

    else:
        mensaje = "Error sintáctico: fin de archivo inesperado"

    errores_sintacticos.append(mensaje)
    print(mensaje)
    
def generar_log_sintactico(usuario):

    ahora = datetime.now()

    nombre_log = (
        f"sintactico-{usuario}-"
        f"{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    )

    carpeta = os.path.join(
        os.path.dirname(__file__),
        '..',
        'logs'
    )

    os.makedirs(carpeta, exist_ok=True)

    ruta = os.path.join(carpeta, nombre_log)

    with open(ruta, "w", encoding="utf-8") as archivo:

        archivo.write("=" * 60 + "\n")
        archivo.write("ANALISIS SINTACTICO DART\n")
        archivo.write(f"Usuario: {usuario}\n")
        archivo.write(
            f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )
        archivo.write("=" * 60 + "\n\n")

        if errores_sintacticos:

            archivo.write("ERRORES SINTACTICOS\n")
            archivo.write("-" * 60 + "\n")

            for error in errores_sintacticos:
                archivo.write(error + "\n")

        else:

            archivo.write(
                "Analisis completado sin errores sintacticos\n"
            )

    print(f"\nLog sintactico generado: {ruta}")
    
parser = yacc.yacc()

def analizar_sintactico(codigo, usuario):

    errores_sintacticos.clear()

    lexer_instance = lex.lex(module=lexer_module)

    parser.parse(codigo, lexer=lexer_instance)

    generar_log_sintactico(usuario)
    
# fin aporte jairo  