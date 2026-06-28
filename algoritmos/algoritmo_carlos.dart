// algoritmo_carlos.dart
// Registra inscripciones a un taller, evita duplicados
// y respeta un cupo maximo de participantes

int calcularCupoDisponible(int maximo, int actuales) {
    return maximo - actuales;
}

void mostrarMensaje(String texto, [int veces = 1]) {
    int contador = 0;
    while (contador < veces) {
        print(texto);
        contador += 1;
    }
}

void main() {
    final int MAX_CUPOS = 3;
    int aceptados = 0;
    int rechazados = 0;
    int duplicados = 0;

    // Nombres ya inscritos, no admite repetidos
    Set<String> inscritos = {};

    // Conteo de resultados por categoria
    Map<String, int> resultados = {
        'aceptados': 0,
        'rechazados': 0,
        'duplicados': 0
    };

    // Solicitudes recibidas en orden de llegada
    List<String> solicitudes = ['Ana', 'Pedro', 'Ana', 'Luis', 'Maria'];

    for (var nombre in solicitudes) {
        if (!inscritos.contains(nombre) && aceptados < MAX_CUPOS) {
            inscritos.add(nombre);
            aceptados += 1;
        } else if (inscritos.contains(nombre)) {
            duplicados += 1;
        } else {
            rechazados += 1;
        }
    }

    resultados['aceptados'] = aceptados;
    resultados['rechazados'] = rechazados;
    resultados['duplicados'] = duplicados;

    int cupoRestante = calcularCupoDisponible(MAX_CUPOS, aceptados);
    int totalProcesados = aceptados + rechazados + duplicados;

    int verificados = 0;
    for (int i = 0; i < aceptados; i += 1) {
        verificados += 1;
    }

    print(cupoRestante);
    print(totalProcesados);
    print(verificados);

    mostrarMensaje('Proceso de inscripcion finalizado');
}
