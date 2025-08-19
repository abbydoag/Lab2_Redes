#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <zlib.h>

using namespace std;

// Función para decodificar Hamming y corregir errores
string decodificarHamming(string mensaje_hamming) {
    int m = mensaje_hamming.size();
    int r = 0;
    while (pow(2, r) < m + r + 1) r++;
    
    vector<int> bits_error;
    
    // Calcular síndrome de error
    for (int i = 0; i < r; i++) {
        int mask = 1 << i;
        int paridad = 0;
        
        for (int j = 0; j < m; j++) {
            if ((j + 1) & mask) {
                paridad ^= (mensaje_hamming[j] - '0');
            }
        }
        
        if (paridad) bits_error.push_back(mask);
    }
    
    // Corregir error si existe
    if (!bits_error.empty()) {
        int error_pos = 0;
        for (int mask : bits_error) error_pos += mask;
        
        if (error_pos <= m) {
            cout << "Error detectado y corregido en posicion " << error_pos << endl;
            mensaje_hamming[error_pos - 1] = (mensaje_hamming[error_pos - 1] == '0') ? '1' : '0';
        }
    }
    
    // Extraer bits de datos (eliminar bits de paridad)
    string mensaje_decodificado;
    int power_of_2 = 1;
    for (int i = 0; i < m; i++) {
        if (i + 1 == power_of_2) {
            power_of_2 *= 2;
        } else {
            mensaje_decodificado += mensaje_hamming[i];
        }
    }
    
    return mensaje_decodificado;
}

int main() {
    cout << "--- RECEPTOR MEJORADO (Hamming + CRC) ---" << endl;
    string trama;
    cout << "Ingrese la trama recibida (mensaje Hamming + CRC): ";
    cin >> trama;

    string mensaje_hamming = trama.substr(0, trama.size() - 32);
    string crc_bin = trama.substr(trama.size() - 32);

    // Calcular CRC
    unsigned long crc_calc = crc32(0L, Z_NULL, 0);
    crc_calc = crc32(crc_calc, reinterpret_cast<const unsigned char*>(mensaje_hamming.c_str()), mensaje_hamming.size());
    unsigned long crc_recv = stoul(crc_bin, nullptr, 2);

    if (crc_recv == crc_calc) {
        string mensaje_original = decodificarHamming(mensaje_hamming);
        cout << "Mensaje recibido correctamente: " << mensaje_original << endl;
    } else {
        cout << "Error detectado: el mensaje no pudo ser corregido" << endl;
    }

    return 0;
}