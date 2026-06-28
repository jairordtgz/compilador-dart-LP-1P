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
    tipo = tipo_desde_token(p.slice[1].type, p[4])
    registrar_variable(p, p[2], tipo, False, p[4], p.lineno(2))
    
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
    tipo = tipo_desde_token(p.slice[2].type, p[5])
    registrar_variable(p, p[3], tipo, True, p[5], p.lineno(3))
    
def p_reasignacion(p):
    '''
    sentencia : IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | IDENTIFICADOR MAS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR MENOS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR PRODUCTO_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR DIVISION_IGUAL valor PUNTO_COMA
    '''
    verificar_declarada(p, p[1], p.lineno(1))
    verificar_modificacion_constante(p, p[1], p.lineno(1))

def p_valor(p):
    '''
    valor : expresion
          | condicion
          | CADENA
          | TRUE
          | FALSE
    '''
    if p.slice[1].type == 'CADENA':
        p[0] = ('String', p[1])
    elif p.slice[1].type in ('TRUE', 'FALSE'):
        p[0] = ('bool', p[1])
    else:
        p[0] = p[1]
    
def p_expresion_parentesis(p):
    '''
    expresion : PAREN_IZQ expresion PAREN_DER
    '''
    p[0] = p[2]
    
def p_operacion_matematica(p):
    '''
    expresion : expresion MAS expresion
              | expresion MENOS expresion
              | expresion PRODUCTO expresion
              | expresion DIVISION expresion
    '''
    tipo = verificar_operacion(p, p[2], p[1], p[3])
    p[0] = (tipo, None)

def p_expresion_valor(p):
    '''
    expresion : ENTERO
              | FLOTANTE
              | IDENTIFICADOR
    '''
    tipo_token = p.slice[1].type
    if tipo_token == 'ENTERO':
        p[0] = ('int', p[1])
    elif tipo_token == 'FLOTANTE':
        p[0] = ('double', p[1])
    else:
        p[0] = (verificar_declarada(p, p[1], p.lineno(1)), None)

def p_condicion_relacional(p):
    '''
    condicion : expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion MAYOR_IGUAL expresion
              | expresion MENOR_IGUAL expresion
              | expresion IGUAL_IGUAL expresion
              | expresion DIFERENTE expresion
    '''
    p[0] = ('bool', None)

def p_condicion_logica(p):
    '''
    condicion : condicion AND condicion
              | condicion OR condicion
    '''
    p[0] = ('bool', None)

def p_condicion_negada(p):
    '''
    condicion : NOT condicion
    '''
    p[0] = ('bool', None)

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

#inicio aporte carlos

# --- Estructura de datos: Mapa ---
def p_declarar_mapa(p):
    '''
    sentencia : MAP_TYPE MENOR STRING_TYPE COMA INT MAYOR IDENTIFICADOR ASIGNACION mapa PUNTO_COMA
              | MAP_TYPE MENOR STRING_TYPE COMA DOUBLE MAYOR IDENTIFICADOR ASIGNACION mapa PUNTO_COMA
              | MAP_TYPE MENOR STRING_TYPE COMA STRING_TYPE MAYOR IDENTIFICADOR ASIGNACION mapa PUNTO_COMA
    '''

def p_mapa(p):
    '''
    mapa : LLAVE_IZQ pares LLAVE_DER
         | LLAVE_IZQ LLAVE_DER
    '''

def p_pares(p):
    '''
    pares : pares COMA par
          | par
    '''

def p_par(p):
    '''
    par : CADENA DOS_PUNTOS valor
    '''

def p_asignar_clave_mapa(p):
    '''
    sentencia : IDENTIFICADOR CORCHETE_IZQ CADENA CORCHETE_DER ASIGNACION valor PUNTO_COMA
    '''

def p_acceder_clave_mapa(p):
    '''
    expresion : IDENTIFICADOR CORCHETE_IZQ CADENA CORCHETE_DER
    '''

# --- Eestructuras de control: else / else if, while ---

def p_if_else(p):
    '''
    sentencia : IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE LLAVE_IZQ sentencias LLAVE_DER
    '''

def p_if_elseif(p):
    '''
    sentencia : IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
              | IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE LLAVE_IZQ sentencias LLAVE_DER
    '''

def p_while(p):
    '''
    sentencia : WHILE PAREN_IZQ condicion PAREN_DER LLAVE_IZQ marca_bucle sentencias LLAVE_DER
    '''
    global profundidad_bucle
    profundidad_bucle -= 1

# --- Tipo de función: void ---

def p_funcion_void(p):
    '''
    sentencia : VOID IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
              | VOID IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
    '''

def p_print(p):
    '''
    sentencia : PRINT PAREN_IZQ valor PAREN_DER PUNTO_COMA
    '''

def p_llamada_funcion_sentencia(p):
    '''
    sentencia : IDENTIFICADOR PAREN_IZQ argumentos PAREN_DER PUNTO_COMA
              | IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTO_COMA
    '''

# Globals para analisis semantico
errores_semanticos = []
tabla_simbolos     = {}   # nombre -> {tipo, constante, valor, linea}
profundidad_bucle  = 0    # contador de bucles anidados (usado también por R6)

# Producción vacía: se reduce al entrar al cuerpo de un bucle,
# incrementando el contador antes de procesar las sentencias internas.
def registrar_variable(p, nombre, tipo, constante, valor, linea):
    tabla_simbolos[nombre] = {
        'tipo':      tipo,
        'constante': constante,
        'valor':     valor,
        'linea':     linea
    }

def verificar_declarada(p, nombre, linea):
    '''R1: la variable debe existir en tabla_simbolos antes de usarse.'''
    if nombre not in tabla_simbolos:
        errores_semanticos.append(
            f"Error semántico [Identificador, Línea {linea}]: "
            f"La variable '{nombre}' no ha sido declarada en el alcance actual."
        )
        return 'desconocido'
    return tabla_simbolos[nombre]['tipo']

def verificar_modificacion_constante(p, nombre, linea):
    '''R2: una variable final/const no puede reasignarse después de su declaración.'''
    if nombre in tabla_simbolos and tabla_simbolos[nombre]['constante']:
        errores_semanticos.append(
            f"Error semántico [Tipo, Línea {linea}]: "
            f"La constante '{nombre}' no puede ser modificada."
        )
        return True
    return False

# fin aporte carlos

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


# fin aporte jairo  


# INICIO APORTE — Benjamin Cedeño


def p_declarar_set(p):
    '''
    sentencia : SET_TYPE MENOR STRING_TYPE MAYOR IDENTIFICADOR ASIGNACION conjunto PUNTO_COMA
              | SET_TYPE MENOR INT MAYOR IDENTIFICADOR ASIGNACION conjunto PUNTO_COMA
    '''

def p_conjunto(p):
    '''
    conjunto : LLAVE_IZQ elementos_conjunto LLAVE_DER
             | LLAVE_IZQ LLAVE_DER
    '''

def p_elementos_conjunto(p):
    '''
    elementos_conjunto : elementos_conjunto COMA valor
                       | valor
    '''

def p_metodo_set(p):
    '''
    sentencia : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ valor PAREN_DER PUNTO_COMA
    '''

def p_llamada_metodo_expresion(p):
    '''
    expresion : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ valor PAREN_DER
    '''

def p_condicion_expresion(p):
    '''
    condicion : expresion
    '''

# --- Estructura de control: for clásico y for-in ---

def p_incremento(p):
    '''
    incremento : IDENTIFICADOR MAS_IGUAL valor
               | IDENTIFICADOR ASIGNACION expresion
    '''

# --- Tipo de función: parámetro opcional con valor por defecto ---

def p_parametro_opcional(p):
    '''
    parametro_opcional : INT IDENTIFICADOR ASIGNACION ENTERO
                       | DOUBLE IDENTIFICADOR ASIGNACION FLOTANTE
                       | STRING_TYPE IDENTIFICADOR ASIGNACION CADENA
    '''

def p_funcion_parametro_opcional(p):
    '''
    sentencia : VOID IDENTIFICADOR PAREN_IZQ parametros COMA CORCHETE_IZQ parametro_opcional CORCHETE_DER PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
              | VOID IDENTIFICADOR PAREN_IZQ CORCHETE_IZQ parametro_opcional CORCHETE_DER PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
    '''

# --- Reglas generales: import e ingreso de datos por teclado ---

def p_import(p):
    '''
    sentencia : IMPORT CADENA PUNTO_COMA
    '''

def p_leer_teclado(p):
    '''
    sentencia : STRING_TYPE INTERROGACION IDENTIFICADOR ASIGNACION IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTO_COMA
    '''

# FIN APORTE — Benjamin Cedeño


def analizar_sintactico(codigo, usuario):

    errores_sintacticos.clear()

    lexer_instance = lex.lex(module=lexer_module)
    
    token_original = lexer_instance.token

    def token_sin_comentarios():
        tok = token_original()
        while tok and tok.type in ('COMENTARIO_LINEA', 'COMENTARIO_BLOQUE'):
            tok = token_original()
        return tok

    lexer_instance.token = token_sin_comentarios

    parser.parse(codigo, lexer=lexer_instance)

    generar_log_sintactico(usuario)


# INICIO APORTE Benjamin Cedeno (Semantico)
errores_semanticos = []
profundidad_bucle = 0   # cuenta cuantos bucles anidados nos rodean

# --- Marca de entrada a un bucle ---
# Produccion vacia: se reduce justo cuando yacc "entra" al
# cuerpo del bucle, antes de procesar las sentencias internas.
def p_marca_inicio_bucle(p):
    '''
    marca_bucle :
    '''
    global profundidad_bucle
    profundidad_bucle += 1

# --- For clasico con marca de bucle ---
def p_for(p):
    '''
    sentencia : FOR PAREN_IZQ sentencia condicion PUNTO_COMA incremento PAREN_DER LLAVE_IZQ marca_bucle sentencias LLAVE_DER
    '''
    global profundidad_bucle
    profundidad_bucle -= 1

# --- For-in con marca de bucle ---
def p_for_in(p):
    '''
    sentencia : FOR PAREN_IZQ VAR IDENTIFICADOR IN IDENTIFICADOR PAREN_DER LLAVE_IZQ marca_bucle sentencias LLAVE_DER
    '''
    global profundidad_bucle
    profundidad_bucle -= 1

# --- Regla 6: break fuera de bucle ---
def p_break(p):
    '''
    sentencia : BREAK PUNTO_COMA
    '''
    if profundidad_bucle == 0:
        linea = p.lineno(1)
        errores_semanticos.append(
            f"Error semantico [Control, Linea {linea}]: "
            f"'break' solo puede usarse dentro de un bucle."
        )

# --- Regla 5: operaciones entre tipos incompatibles ---
# Esta funcion auxiliar evita que el programa truene si una
# expresion todavia no trae tipo definido (por compatibilidad
# con reglas que aÃºn no propagan tipo).
def _tipo_de(valor):
    if isinstance(valor, tuple) and len(valor) == 2:
        return valor[0]
    return 'desconocido'

def tipo_desde_token(token, valor=None):
    tipos = {
        'INT': 'int',
        'DOUBLE': 'double',
        'STRING_TYPE': 'String',
        'BOOL': 'bool'
    }
    if token == 'VAR':
        return _tipo_de(valor)
    return tipos.get(token, 'desconocido')

def verificar_operacion(p, operador, izquierda, derecha):
    tipo_izq = _tipo_de(izquierda)
    tipo_der = _tipo_de(derecha)
    numericos = ('int', 'double')

    if tipo_izq in numericos and tipo_der in numericos:
        return 'double' if 'double' in (tipo_izq, tipo_der) else 'int'

    if tipo_izq != 'desconocido' and tipo_der != 'desconocido':
        linea = p.lineno(2)
        errores_semanticos.append(
            f"Error semantico [Operacion, Linea {linea}]: "
            f"El operador '{operador}' no es compatible entre "
            f"tipos '{tipo_izq}' y '{tipo_der}'."
        )
    return 'error'


parser = yacc.yacc()

# --- Log semantico ---
def generar_log_semantico(usuario):
    ahora = datetime.now()
    nombre_log = f"semantico-{usuario}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"

    carpeta = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre_log)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("=" * 60 + "\n")
        archivo.write("ANALISIS SEMANTICO DART\n")
        archivo.write(f"Usuario: {usuario}\n")
        archivo.write(f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n")
        archivo.write("=" * 60 + "\n\n")

        if errores_semanticos:
            archivo.write("ERRORES SEMANTICOS\n")
            archivo.write("-" * 60 + "\n")
            for error in errores_semanticos:
                archivo.write(error + "\n")
        else:
            archivo.write("Analisis completado sin errores semanticos\n")

    print(f"\nLog semantico generado: {ruta}")

def analizar_semantico(codigo, usuario):
    global profundidad_bucle
    errores_semanticos.clear()
    tabla_simbolos.clear()
    profundidad_bucle = 0

    lexer_instance = lex.lex(module=lexer_module)
    token_original = lexer_instance.token

    def token_sin_comentarios():
        tok = token_original()
        while tok and tok.type in ('COMENTARIO_LINEA', 'COMENTARIO_BLOQUE'):
            tok = token_original()
        return tok

    lexer_instance.token = token_sin_comentarios
    parser.parse(codigo, lexer=lexer_instance)
    generar_log_semantico(usuario)


# FIN APORTE Benjamin Cedeno (Semantico)



