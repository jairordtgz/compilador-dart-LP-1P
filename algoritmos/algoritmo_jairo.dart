int sumar(int a, int b) {
  return a + b;
}

double calcularPromedio(double n1, double n2) {
  return (n1 + n2) / 2;
}

List<double> notas = [7.5, 8.0, 9.5];
List<String> nombres = ["Jairo", "Dylan", "Ellen"];
int edad = 25;
double precio = 9.99;
String nombre = "JairoRodriguez";
bool activo = true;
double x = 0; 
final int MAX = 100;
const double PI = 3.14159;

x += 1;
x -= 0;
x *= 1;
x /= 1;

bool esMayor = edad >= 18;
bool esIgual = edad == 25;
bool esDiferente = precio != 0.0;
bool esMenor = precio < 100;
bool esMenorIgual = precio <= 9.99;
bool esMayorQ = precio > 5.0;
bool esAlto = edad >= 18;

int nivel = 3;
double nota = 87.5;
bool aprobado = nota >= 60.0;
bool reprobado = nota < 60.0;
bool exacto = nota == 87.5;
bool distinto = nivel != 0;

int resultado = sumar(10, 5);
double promedio = calcularPromedio(80.0, 95.0);

String mensaje = "Prueba completada";