import "mi_lib";

int suma = 10 + 5;
int resta = 10 - 5;
double division = 10 / 5;

// Set y método sobre set
Set<String> conjunto = {"dart", "python"};
conjunto.add("rust");

// Lista
List<int> numeros = [1, 2, 3];

// Map y asignación por clave
Map<String, int> mapa = {"uno": 1};
mapa["uno"] = 2;

// Función con parámetro opcional (por defecto)
void opcion([int x = 5]) {
    int tmp = x;
}

// Función int con return
int sumar(int a, int b) { return a + b; }

int resultado = sumar(2, 3);
