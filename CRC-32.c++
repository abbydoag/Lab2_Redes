#include <iostream>
#include <string>
#include <bitset>
using namespace std;

// Polinomio generador estándar de CRC-32
const unsigned int POLY = 0x04C11DB7;

// Función que calcula CRC-32 sobre un string binario
unsigned int calcularCRC32(const string &bits) {
    unsigned int crc = 0xFFFFFFFF; // Valor inicial

    for (char c : bits) {
        int bit = (c == '1') ? 1 : 0;
        crc ^= (bit << 31); // Colocar bit en la parte más alta del CRC

        for (int i = 0; i < 1; i++) { // Avanza 1 bit
            if (crc & 0x80000000) {
                crc = (crc << 1) ^ POLY;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFF; // XOR final
}

int main() {
    cout << "--- RECEPTOR CRC-32 ---" << endl;

    string recibido;
    cout << "Ingrese el mensaje recibido (mensaje + CRC en binario): ";
    cin >> recibido;

    // Calcular CRC del mensaje recibido
    unsigned int crc = calcularCRC32(recibido);

    if (crc == 0) {
        cout << "✅ No se detectaron errores." << endl;
        // Mostrar solo la parte original (sin los 32 bits de CRC al final)
        string original = recibido.substr(0, recibido.size() - 32);
        cout << "Mensaje original: " << original << endl;
    } else {
        cout << "❌ Se detectaron errores. El mensaje se descarta." << endl;
    }

    return 0;
}
