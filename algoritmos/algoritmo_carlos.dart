// algoritmo_carlos.dart

/* Verificar si un número es par o impar */
void verificar(int numero) {
    bool esPar = false;

    //Resultado de la verificación
    int resultado = numero % 2;

    if(resultado == 0) {
        esPar = true;
    }

    /* Impresion del resultado
    de la operación*/

    if (esPar) {
        print('Es par.');
    } else {
        print('Es impar.');
    }

}

void main() {
    //Lista de numeros
    List<int> numeros = [1, 2, 3, 4];

    //Verificando todos los numeros de la lista
    for (var numero in numeros) {
        verificar(numero);
    }
}