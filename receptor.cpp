#include <iostream>
#include <string>
#include <zlib.h>  
using namespace std;

int main() {
    cout << "--- RECEPTOR CRC-32 ---" << endl;
    string trama;
    cout << "Ingrese la trama recibida (mensaje Hamming + CRC): ";
    cin >> trama;

    // Separar mensaje Hamming y CRC
    string mensaje_hamming = trama.substr(0, trama.size() - 32);
    string crc_bin = trama.substr(trama.size() - 32);

    // Calcular CRC-32 sobre el mensaje recibido
    unsigned long crc_calc = crc32(0L, Z_NULL, 0);
    crc_calc = crc32(crc_calc, reinterpret_cast<const unsigned char*>(mensaje_hamming.c_str()), mensaje_hamming.size());

    // Pasar CRC recibido a número
    unsigned long crc_recv = stoul(crc_bin, nullptr, 2);

    // Verificar si hay errores
    if (crc_recv == crc_calc) {
        cout << " No se detectaron errores en la transmisión." << endl;
        cout << "Mensaje Hamming recibido: " << mensaje_hamming << endl;
    } else {
        cout << " Error detectado: el mensaje se descarta." << endl;
    }

    return 0;
}
