import zlib

# -----------------------------
# FUNCIONES DE HAMMING
# -----------------------------

def bitsParidad(m): 
    """Calcula el número de bits de paridad necesarios"""
    for r in range(1, 50):
        if 2**r >= m + r + 1:
            return r

def bitPosicionParidad(mensaje, r):
    """Coloca los bits de paridad en las posiciones correspondientes"""
    m = len(mensaje)
    res = []
    mensaje_index = 0
    for i in range(1, m + r + 1):
        if (i & (i - 1)) == 0:
            res.append("0")  # bit de paridad temporal
        else:
            if mensaje_index < m:
                res.append(mensaje[mensaje_index])
                mensaje_index += 1
            else:
                res.append("0")
    return res

def bitsParidadCalculo(bits, r):
    """Calcula los valores correctos de los bits de paridad"""
    bits = list(bits)
    for i in range(r):
        pos = 2**i - 1
        if pos >= len(bits):
            continue
        paridad = 0
        for j in range(pos, len(bits), 2**(i+1)):
            for k in range(j, min(j + 2**i, len(bits))):
                if k != pos:
                    paridad ^= int(bits[k])
        bits[pos] = str(paridad)
    return "".join(bits)

def hammingCodif(mensaje):
    """Codifica un mensaje binario con Hamming"""
    r = bitsParidad(len(mensaje))
    posiciones = bitPosicionParidad(mensaje, r)
    return bitsParidadCalculo(posiciones, r)

def esBinario(cadena):
    """Verifica si una cadena contiene solo 0 y 1"""
    return all(c in '01' for c in cadena)

# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------

def main():
    print("--- EMISOR HAMMING + CRC ---")
    
    # Entrada de mensaje binario
    while True:
        mensaje = input("Ingrese el mensaje binario: ")
        if esBinario(mensaje):
            break
        else:
            print("Error, solo se aceptan 0 y 1")
    
    # Codificación Hamming
    hamming = hammingCodif(mensaje)
    
    # CRC-32 del mensaje codificado
    crc = zlib.crc32(hamming.encode())
    crc_bin = format(crc, "032b")  # Representación binaria de 32 bits
    
    # Trama final = mensaje codificado + CRC
    trama = hamming + crc_bin
    
    # Mostrar resultados
    print("\n--- DETALLES DE Hamming ---")
    for i, bit in enumerate(hamming, 1):
        if (i & (i - 1)) == 0:
            print(f"Bit {i}: [P] = {bit}")
        else:
            print(f"Bit {i}: [M] = {bit}")
    
    print("\n--- RESULTADOS FINALES ---")
    print("Mensaje original:", mensaje)
    print("Mensaje codificado Hamming:", hamming)
    print("CRC-32 en binario:", crc_bin)
    print("TRAMA FINAL (enviar al receptor):", trama)
    print(f"Bits de paridad añadidos: {len(hamming) - len(mensaje)}")

if __name__ == "__main__":
    main()
