#EMISOR
#Hamming: Corrección de errores

def bitsParidad(m): 
    for r in range (1,50): #50 por simplificar
        if(2**r>=m+r+1):#formula bits de paridad 
            return r
        
def bitPosicionParidad(mensaje, r):
    #colocar bits paridad y de la cadena donde corresponden
    m = len(mensaje)
    res = []
    mensaje_index = 0

    #potencia de 2 (paridad)
    for i in range(1, m+r+1):
        if(i & (i-1)) == 0:
            res.append("0") #temp
        #bits mensaje
        else:
            if mensaje_index < m:
                res.append(mensaje[mensaje_index])
                mensaje_index += 1
            else:
                res.append("0")
    return res

def bitsParidadCalculo(bits, r):
    bits = list(bits) #lista

    for i in range(r):
        pos = 2**i-1 #posicion bit paridad
        if pos >= len(bits):
            continue
        paridad = 0
        #XOR
        for j in range(pos, len(bits), 2**(i+1)):
            for k in range(j, min(j + 2**i, len(bits))):
                if k != pos: #no inlcuye el de paridad
                    paridad ^= int(bits[k])
        bits[pos] = str(paridad)
    return "".join(bits)

def hammingCodif(mensaje):
    r = bitsParidad(len(mensaje))
    posiciones = bitPosicionParidad(mensaje, r)
    return bitsParidadCalculo(posiciones, r)

def esBinario(cadena):
    return all(c in '01' for c in cadena)

def main():
    print("--- ALGORITMO DE HAMMING ---")
    while True:
        mensaje = input("Ingrese el mensaje binario: ")
        if esBinario(mensaje):
            break
        else:
            print("Error, por favor ingrese un mensaje y binario (1 y 0)")

    #Hamming
    hamming = hammingCodif(mensaje)
    for i, bit in enumerate(hamming, 1):
        if (i & (i - 1)) == 0:  #Pot. 2
            print(f"Bit {i}: [P] = {bit}")
        else:
            print(f"Bit {i}: [M] = {bit}")
    
    print("\nRESULTADO:")
    print(f"Mensaje original:  {mensaje} (Longitud: {len(mensaje)} bits)")
    print(f"Mensaje codificado: {hamming} (Longitud: {len(hamming)} bits)")
    print(f"Bits de paridad añadidos: {len(hamming)-len(mensaje)}")

    

if __name__ == "__main__":
    main()