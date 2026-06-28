import sys
import os

# <Carlos Lopez>

CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CURRENT_DIR)

from parser import analizar_semantico

DESARROLLADORES = {
    'Carlos':   ('caluloper',   'algoritmo_carlos.dart'),
    'Jairo':    ('jairordtgz',  'algoritmo_jairo.dart'),
    'Benjamin': ('ibcg04',      'algoritmo_benjamin.dart'),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in DESARROLLADORES:
        print('Uso: python run_semantico.py [Carlos | Jairo | Benjamin]')
        sys.exit(1)

    clave = sys.argv[1]
    desarrollador, archivo = DESARROLLADORES[clave]

    ruta = os.path.join(PROJECT_ROOT, 'algoritmos', archivo)

    if not os.path.exists(ruta):
        print(f'[Error] No se encontró: {ruta}')
        sys.exit(1)

    with open(ruta, 'r', encoding='utf-8') as f:
        codigo = f.read()

    print('=' * 64)
    print(f'  Archivo : {archivo}')
    print(f'  Autor   : {desarrollador}')
    print('=' * 64)

    analizar_semantico(codigo, desarrollador)

if __name__ == '__main__':
    main()

# </Carlos Lopez>
