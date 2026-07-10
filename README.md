# Compilador de Dart — Analizador Léxico, Sintáctico y Semántico
Implementa un analizador léxico, sintáctico y semántico para un subconjunto
de Dart, usando PLY (Python Lex-Yacc), con interfaz gráfica en Tkinter.

## Integrantes

| Integrante | GitHub | Responsabilidad |
|---|---|---|
| Carlos López | @caluloper | Léxico (identificadores, delimitadores, comentarios), Map, if/else/while, función void, Semántico R1/R2 |
| Jairo Rodríguez | @jairordtgz | Léxico (literales, relacionales, asignación), for/for-in, List, función con retorno, Semántico R3/R4 |
| Benjamin Cedeño | @ibcg04 | Léxico (aritméticos, lógicos, errores), Set, función con parámetro opcional, import/input, Semántico R5/R6 |

## Requisitos

- Python 3.10 o superior
- Tkinter (incluido por defecto en la mayoría de instalaciones de Python en Windows/Mac; en Linux puede requerir `sudo apt install python3-tk`)

## Instalación

```bash
pip install ply
```

## Cómo ejecutar

### Interfaz gráfica (recomendado)

```bash
python gui/interfaz_grafica.py
```

### Por consola (análisis individual)

```bash
cd lexer
python run_lexer.py [Carlos | Jairo | Benjamin]

cd ../parser
python run_parser.py [Carlos | Jairo | Benjamin]
python run_semantico.py [Carlos | Jairo | Benjamin]
```

Cada ejecución genera un log en `/logs` con el formato:
`{tipo}-{usuario}-{fecha}-{hora}.txt`
