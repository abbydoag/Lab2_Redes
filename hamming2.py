import random
import zlib
import matplotlib.pyplot as plt
from math import log2, ceil
import numpy as np

# --- Configuración Global ---
N_PRUEBAS = 10000  # Número de pruebas por experimento
TAMANOS_MENSAJE = [8, 16, 32, 64]  # Tamaños a probar
PROBABILIDADES_ERROR = [0, 0.01, 0.05, 0.1, 0.2]  # Probabilidades de error a evaluar

# --- Funciones de Codificación Hamming ---

def calcular_bits_paridad(m):
    """Calcula el número necesario de bits de paridad para un mensaje de longitud m"""
    r = 0
    while 2**r < m + r + 1:
        r += 1
    return r

def insertar_posiciones_paridad(mensaje, r):
    """Inserta ceros en las posiciones de los bits de paridad"""
    m = len(mensaje)
    resultado = []
    indice_mensaje = 0
    
    for i in range(1, m + r + 1):
        if i & (i - 1) == 0:  # Si es potencia de 2
            resultado.append('0')
        else:
            if indice_mensaje < m:
                resultado.append(mensaje[indice_mensaje])
                indice_mensaje += 1
            else:
                resultado.append('0')  # Relleno si es necesario
    return resultado

def calcular_bits_paridad_valores(bits, r):
    """Calcula los valores de los bits de paridad"""
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
    return ''.join(bits)

def codificar_hamming(mensaje):
    """Codifica un mensaje usando código Hamming"""
    r = calcular_bits_paridad(len(mensaje))
    posiciones = insertar_posiciones_paridad(mensaje, r)
    return calcular_bits_paridad_valores(posiciones, r)

# --- Funciones CRC ---

def calcular_crc32(mensaje):
    """Calcula el CRC-32 de un mensaje y lo devuelve como cadena binaria de 32 bits"""
    crc = zlib.crc32(mensaje.encode())
    return format(crc, "032b")

# --- Funciones Auxiliares ---

def generar_mensaje_aleatorio(longitud):
    """Genera una cadena binaria aleatoria de la longitud especificada"""
    return ''.join(random.choice('01') for _ in range(longitud))

def introducir_errores(trama, probabilidad_error):
    """Introduce errores aleatorios en la trama según la probabilidad dada"""
    return ''.join(
        '1' if bit == '0' and random.random() < probabilidad_error else
        '0' if bit == '1' and random.random() < probabilidad_error else
        bit
        for bit in trama
    )

# --- Funciones de Prueba y Simulación ---

def ejecutar_prueba(N, longitud, prob_error, modo='hamming_crc'):
    """
    Ejecuta una prueba de transmisión con los parámetros dados
    Modos disponibles: 'solo_crc', 'solo_hamming', 'hamming_crc'
    """
    correctos = 0
    detectados = 0
    no_detectados = 0
    
    for _ in range(N):
        # Generar mensaje original
        mensaje = generar_mensaje_aleatorio(longitud)
        
        # Codificación según el modo seleccionado
        if modo == 'solo_crc':
            crc = calcular_crc32(mensaje)
            trama = mensaje + crc
        elif modo == 'solo_hamming':
            trama = codificar_hamming(mensaje)
        else:  # 'hamming_crc' (default)
            hamming = codificar_hamming(mensaje)
            crc = calcular_crc32(hamming)
            trama = hamming + crc
        
        # Introducir errores
        trama_recibida = introducir_errores(trama, prob_error)
        
        # Verificación según el modo
        if modo == 'solo_crc':
            mensaje_recibido = trama_recibida[:-32]
            crc_recibido = trama_recibida[-32:]
            crc_calculado = calcular_crc32(mensaje_recibido)
            
            if crc_recibido == crc_calculado:
                correctos += 1
            else:
                detectados += 1
        
        elif modo == 'solo_hamming':
            
            mensaje_original = mensaje
            mensaje_recibido = trama_recibida
            if mensaje_recibido == trama:
                correctos += 1
            else:
                detectados += 1
        
        else:  
            mensaje_hamming = trama_recibida[:-32]
            crc_recibido = trama_recibida[-32:]
            crc_calculado = calcular_crc32(mensaje_hamming)
            
            if crc_recibido == crc_calculado:
                correctos += 1
            else:
                detectados += 1
    
    no_detectados = N - correctos - detectados
    
    return {
        "enviados": N,
        "correctos": correctos,
        "detectados": detectados,
        "no_detectados": no_detectados,
        "tasa_deteccion": detectados/(N - correctos) if (N - correctos) > 0 else 1.0,
        "tasa_no_detectados": no_detectados/N if N > 0 else 0,
        "eficiencia": correctos/N,
        "overhead": (len(trama) - longitud)/longitud if longitud > 0 else 0
    }

# --- Funciones de Visualización ---

def graficar_eficiencia_vs_error(tamanos=[16]):
    """Genera gráfica de eficiencia vs probabilidad de error para diferentes tamaños"""
    plt.figure(figsize=(12, 6))
    
    for tam in tamanos:
        eficiencias = []
        for p in PROBABILIDADES_ERROR:
            res = ejecutar_prueba(N_PRUEBAS, tam, p)
            eficiencias.append(res['eficiencia'])
        
        plt.plot(PROBABILIDADES_ERROR, eficiencias, marker='o', label=f'Tamaño {tam} bits')
    
    plt.title("Eficiencia de Transmisión vs Probabilidad de Error")
    plt.xlabel("Probabilidad de Error por Bit")
    plt.ylabel("Eficiencia (Mensajes Correctos/Enviados)")
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_tamanos_vs_eficiencia(prob_error=0.1):
    """Genera gráfica de eficiencia vs tamaño de mensaje"""
    eficiencias = []
    overheads = []
    
    for tam in TAMANOS_MENSAJE:
        res = ejecutar_prueba(N_PRUEBAS, tam, prob_error)
        eficiencias.append(res['eficiencia'])
        overheads.append(res['overhead'])
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Tamaño del Mensaje (bits)')
    ax1.set_ylabel('Eficiencia', color=color)
    ax1.plot(TAMANOS_MENSAJE, eficiencias, marker='o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Overhead (Redundancia)', color=color)
    ax2.plot(TAMANOS_MENSAJE, overheads, marker='s', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title(f"Eficiencia y Overhead vs Tamaño del Mensaje (Error={prob_error*100}%)")
    plt.grid(True)
    plt.show()

def comparar_algoritmos(tam=16):
    """Compara los diferentes algoritmos de detección/corrección de errores"""
    modos = ['solo_crc', 'solo_hamming', 'hamming_crc']
    nombres = ['Solo CRC-32', 'Solo Hamming', 'Hamming + CRC']
    
    plt.figure(figsize=(12, 6))
    
    for modo, nombre in zip(modos, nombres):
        eficiencias = []
        detecciones = []
        
        for p in PROBABILIDADES_ERROR:
            res = ejecutar_prueba(N_PRUEBAS, tam, p, modo)
            eficiencias.append(res['eficiencia'])
            detecciones.append(res['tasa_deteccion'])
        
        plt.plot(PROBABILIDADES_ERROR, eficiencias, marker='o', label=nombre)
    
    plt.title(f"Comparación de Algoritmos (Mensaje de {tam} bits)")
    plt.xlabel("Probabilidad de Error por Bit")
    plt.ylabel("Eficiencia (Mensajes Correctos/Enviados)")
    plt.legend()
    plt.grid(True)
    plt.show()

def mostrar_metricas_completas(tam=16, prob_error=0.1):
    """Muestra un reporte completo de métricas para una configuración dada"""
    print("\n=== REPORTE DE MÉTRICAS ===")
    print(f"Configuración: Mensaje de {tam} bits, Prob. error = {prob_error*100}%")
    print(f"Número de pruebas: {N_PRUEBAS}")
    
    resultados = ejecutar_prueba(N_PRUEBAS, tam, prob_error)
    
    print("\n--- Resultados ---")
    print(f"Mensajes correctamente recibidos: {resultados['correctos']} ({resultados['eficiencia']:.2%})")
    print(f"Errores detectados: {resultados['detectados']} ({resultados['tasa_deteccion']:.2%} de los errores)")
    print(f"Errores no detectados: {resultados['no_detectados']} ({resultados['tasa_no_detectados']:.2%})")
    print(f"Overhead de redundancia: {resultados['overhead']:.2%}")

# --- Ejecución Principal ---

if __name__ == "__main__":
    print("=== SISTEMA DE COMUNICACIÓN CON DETECCIÓN/CORRECCIÓN DE ERRORES ===")
    print("=== Versión mejorada con análisis completo ===")
    
    # Gráfica principal: Eficiencia vs Probabilidad de error
    print("\nGenerando gráfica: Eficiencia vs Probabilidad de error...")
    graficar_eficiencia_vs_error(tamanos=[8, 16, 32])
    
    # Gráfica de tamaño vs eficiencia
    print("\nGenerando gráfica: Tamaño del mensaje vs Eficiencia...")
    graficar_tamanos_vs_eficiencia(prob_error=0.1)
    
    # Comparación de algoritmos
    print("\nGenerando comparación de algoritmos...")
    comparar_algoritmos(tam=16)
    
    # Reporte de métricas
    print("\nGenerando reporte de métricas detallado...")
    mostrar_metricas_completas(tam=16, prob_error=0.1)
    
    print("\n=== ANÁLISIS COMPLETADO ===")