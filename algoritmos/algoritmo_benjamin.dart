// Prueba de operadores logicos y matematicos - Benjamin Cedeño

int suma = 10 + 5;
int resta = 10 - 5;
int multiplicacion = 10 * 5;
double division = 10 / 5;
int division_entera = 10 ~/ 3;
int modulo = 10 % 3;

bool and_logico = true && false;
bool or_logico = true || false;
bool not_logico = !true;

// Estructuras asignadas para las siguientes fases
Set<String> lenguajes = {'dart', 'python'};

int contador = 0;
while(contador < 5) {
    if (contador == 3) {
        break;
    } else {
        contador = contador + 1;
    }
}

// Error lexico intencional para probar la funcion t_error
@ variable_invalida = 100;