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
    tipo_token = p.slice[1].type
    nombre = p[2]
    valor  = p[4]
    linea  = p.lineno(2)

    if tipo_token == 'VAR':
        tipo_final = valor[0] if valor else 'desconocido'
    else:
        tipo_final = TOKEN_A_TIPO[tipo_token]
        verificar_tipo_asignacion(p, nombre, tipo_final, valor, linea)

    registrar_variable(p, nombre, tipo_final, constante=False,
                        valor=(valor[1] if valor else None), linea=linea)
    
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
    
    tipo_token = p.slice[2].type
    nombre = p[3]
    valor  = p[5]
    linea  = p.lineno(3)

    tipo_final = TOKEN_A_TIPO[tipo_token]
    verificar_tipo_asignacion(p, nombre, tipo_final, valor, linea)

    registrar_variable(p, nombre, tipo_final, constante=True,
                        valor=(valor[1] if valor else None), linea=linea)
    
def p_reasignacion(p):
    '''
    sentencia : IDENTIFICADOR ASIGNACION valor PUNTO_COMA
              | IDENTIFICADOR MAS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR MENOS_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR PRODUCTO_IGUAL valor PUNTO_COMA
              | IDENTIFICADOR DIVISION_IGUAL valor PUNTO_COMA
    '''
    nombre = p[1]
    valor  = p[3]
    linea  = p.lineno(1)

    tipo_var      = verificar_declarada(p, nombre, linea)             
    es_constante  = verificar_modificacion_constante(p, nombre, linea) 

    if not es_constante and tipo_var != 'desconocido':                
        verificar_tipo_asignacion(p, nombre, tipo_var, valor, linea)

#inicio avance 3 (semantico): Jairo Rodriguez
TOKEN_A_TIPO = {
    'INT':         'int',
    'DOUBLE':      'double',
    'STRING_TYPE': 'String',
    'BOOL':        'bool',
}

def tipos_compatibles(tipo_declarado, tipo_valor):
    '''Dart permite asignar int a una variable double (ensanchamiento
       numérico, válido para literales). El resto exige tipo exacto.'''
    if tipo_declarado == tipo_valor:
        return True
    if tipo_declarado == 'double' and tipo_valor == 'int':
        return True
    return False

#regla semantica 3
def verificar_tipo_asignacion(p, nombre, tipo_declarado, valor, linea):
    if valor is None:
        return None
    tipo_valor, dato = valor
    if tipo_valor == 'desconocido':
        return dato  
    if not tipos_compatibles(tipo_declarado, tipo_valor):
        errores_semanticos.append(
            f"Error semántico [Tipo, Línea {linea}]: "
            f"No se puede asignar un valor de tipo '{tipo_valor}' "
            f"a la variable '{nombre}' de tipo '{tipo_declarado}'."
        )
    return dato

#regla semantica 4
def verificar_tipo_retorno(p, nombre_funcion, tipo_esperado, valor_retorno, linea):
    if valor_retorno is None:
        return
    tipo_valor, _ = valor_retorno
    if tipo_valor == 'desconocido':
        return
    if not tipos_compatibles(tipo_esperado, tipo_valor):
        errores_semanticos.append(
            f"Error semántico [Retorno, Línea {linea}]: "
            f"La función '{nombre_funcion}' debe retornar un valor de tipo "
            f"'{tipo_esperado}', pero se encontró '{tipo_valor}'."
        )

#fin avance 3 semantico Jairo Rodriguez

def p_valor(p):
    '''
    valor : expresion
          | condicion
          | CADENA
          | TRUE
          | FALSE
    '''
    tipo_token = p.slice[1].type
    if tipo_token == 'expresion':
        p[0] = p[1]
    elif tipo_token == 'condicion':
        p[0] = ('bool', None)
    elif tipo_token == 'CADENA':
        p[0] = ('String', p[1])
    elif tipo_token == 'TRUE':
        p[0] = ('bool', True)
    elif tipo_token == 'FALSE':
        p[0] = ('bool', False)
    
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
    p[0] = (verificar_operacion(p, p[2], p[1], p[3]), None)
    

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
        nombre = p[1]
        linea  = p.lineno(1)
        tipo_var = verificar_declarada(p, nombre, linea)
        p[0] = (tipo_var, nombre)
    
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
              | INT IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ sentencias RETURN expresion PUNTO_COMA LLAVE_DER
              | INT IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ sentencias RETURN expresion PUNTO_COMA LLAVE_DER
    '''

    nombre_funcion = p[2]
    expresion_retorno = p[len(p) - 3]
    verificar_tipo_retorno(p, nombre_funcion, 'int', expresion_retorno, p.lineno(1))

def p_funcion_double(p):
    '''
    sentencia : DOUBLE IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
              | DOUBLE IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ RETURN expresion PUNTO_COMA LLAVE_DER
              | DOUBLE IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ sentencias RETURN expresion PUNTO_COMA LLAVE_DER
              | DOUBLE IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ sentencias RETURN expresion PUNTO_COMA LLAVE_DER
    '''

    nombre_funcion = p[2]
    expresion_retorno = p[len(p) - 3]
    verificar_tipo_retorno(p, nombre_funcion, 'double', expresion_retorno, p.lineno(1))
    
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
    tipo_token = p.slice[1].type
    nombre = p[2]
    tipo   = TOKEN_A_TIPO[tipo_token]
    registrar_variable(p, nombre, tipo, constante=False,
                        valor=None, linea=p.lineno(2))
    p[0] = (tipo, nombre)

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
              | IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER resto_if
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
    
def p_acceder_indice_lista(p):
    '''
    expresion : IDENTIFICADOR CORCHETE_IZQ expresion CORCHETE_DER
    '''
    p[0] = ('desconocido', None)

# --- Eestructuras de control: else / else if (cadena de largo arbitrario), while ---

def p_resto_if(p):
    '''
    resto_if : ELSE IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
             | ELSE IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER resto_if
             | ELSE LLAVE_IZQ sentencias LLAVE_DER
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

# --- Operadores aritméticos adicionales ---
def p_operacion_modulo(p):
    '''
    expresion : expresion MODULO expresion
    '''
    p[0] = (verificar_operacion(p, p[2], p[1], p[3]), None)

def p_operacion_division_entera(p):
    '''
    expresion : expresion DIVISION_ENTERA expresion
    '''
    p[0] = (verificar_operacion(p, p[2], p[1], p[3]), None)

# --- Valor nulo ---
def p_valor_null(p):
    '''
    valor : NULL
    '''
    p[0] = ('desconocido', None)

# --- Tipo dynamic ---
def p_declarar_dynamic(p):
    '''
    sentencia : DYNAMIC IDENTIFICADOR ASIGNACION valor PUNTO_COMA
    '''
    nombre = p[2]
    valor  = p[4]
    linea  = p.lineno(2)
    registrar_variable(p, nombre, 'desconocido', constante=False,
                        valor=(valor[1] if valor else None), linea=linea)

# --- Continue ---
def p_continue(p):
    '''
    sentencia : CONTINUE PUNTO_COMA
    '''

# --- Comentarios (filtrados por el wrapper antes de llegar al parser) ---
def p_comentario(p):
    '''
    sentencia : COMENTARIO_LINEA
              | COMENTARIO_BLOQUE
    '''

# Globals para analisis semantico
errores_semanticos = []
tabla_simbolos     = {}   # nombre -> {tipo, constante, valor, linea}
profundidad_bucle  = 0    # contador de bucles anidados (usado también por R6)

# Producción vacía: se reduce al entrar al cuerpo de un bucle,
# incrementando el contador antes de procesar las sentencias internas.
def p_marca_inicio_bucle(p):
    '''
    marca_bucle :
    '''
    global profundidad_bucle
    profundidad_bucle += 1

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
    tipo_token = p.slice[1].type
    nombre = p[2]
    tipo   = TOKEN_A_TIPO[tipo_token]
    registrar_variable(p, nombre, tipo, constante=False,
                        valor=None, linea=p.lineno(2))

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
    registrar_variable(p, p[3], 'String', constante=False,
                        valor=None, linea=p.lineno(3))

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


#inicio aporte carlos

def generar_log_semantico(usuario):

    ahora      = datetime.now()
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

# fin aporte carlos


# INICIO APORTE Benjamin Cedeño (Semántico)

# --- For clásico con marca de bucle ---
def p_for(p):
    '''
    sentencia : FOR PAREN_IZQ sentencia condicion PUNTO_COMA incremento PAREN_DER LLAVE_IZQ marca_bucle sentencias LLAVE_DER
    '''
    global profundidad_bucle
    profundidad_bucle -= 1

# --- For-in con marca de bucle ---
def p_encabezado_for_in(p):
    '''
    encabezado_for_in : FOR PAREN_IZQ VAR IDENTIFICADOR IN IDENTIFICADOR PAREN_DER
    '''
    # Se reduce ANTES de entrar al cuerpo del for-in, por eso aqui si
    # es seguro registrar la variable de iteracion (evita falsos R1
    # cuando el cuerpo del bucle usa esa variable, ej: print(n)).
    registrar_variable(p, p[4], 'desconocido', constante=False,
                        valor=None, linea=p.lineno(4))

def p_for_in(p):
    '''
    sentencia : encabezado_for_in LLAVE_IZQ marca_bucle sentencias LLAVE_DER
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
            f"Error semántico [Control, Línea {linea}]: "
            f"'break' solo puede usarse dentro de un bucle."
        )

# --- Regla 5: operaciones entre tipos incompatibles ---
# Esta función auxiliar evita que el programa truene si una
# expresion todavía no trae tipo definido (por compatibilidad
# con reglas que aún no propagan tipo).
def _tipo_de(valor):
    if isinstance(valor, tuple) and len(valor) == 2:
        return valor[0]
    return 'desconocido'

def verificar_operacion(p, operador, izquierda, derecha):
    tipo_izq = _tipo_de(izquierda)
    tipo_der = _tipo_de(derecha)
    numericos = ('int', 'double')

    if tipo_izq in numericos and tipo_der in numericos:
        return 'double' if 'double' in (tipo_izq, tipo_der) else 'int'

    if tipo_izq != 'desconocido' and tipo_der != 'desconocido':
        linea = p.lineno(2)
        errores_semanticos.append(
            f"Error semántico [Operación, Línea {linea}]: "
            f"El operador '{operador}' no es compatible entre "
            f"tipos '{tipo_izq}' y '{tipo_der}'."
        )
    return 'desconocido'

parser = yacc.yacc()
