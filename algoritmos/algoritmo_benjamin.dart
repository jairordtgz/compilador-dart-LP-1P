import "mi_lib";

int numero = 10;
double decimal = 2.5;
String texto = "dart";

int suma = numero + 5;
double mezclaNumerica = numero + decimal;

// Error de prueba comentado:
// Operacion incompatible entre String e int.
// var operacionIncompatible = texto + numero;

int i = 0;
for (i = 0; i < 3; i += 1) {
    int dentroFor = i + 1;
    break;
}

List<int> numeros = [1, 2, 3];
for (var item in numeros) {
    int recorrido = 1;
}

while (numero > 0) {
    numero -= 1;
    break;
}

// Error de prueba comentado:
// break fuera de un bucle.
// break;
