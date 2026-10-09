
from pathlib import Path
from PIL import Image
import numpy as np
import time

from quadtree import construir_quadtree


# Carpetas del proyecto
CARPETA_IMAGENES = Path("imagenes")
CARPETA_RESULTADOS = Path("resultados")

CARPETA_IMAGENES.mkdir(exist_ok=True)
CARPETA_RESULTADOS.mkdir(exist_ok=True)


def contar_nodos(nodo):
    """Cuenta todos los nodos del arbol."""
    return 1 + sum(
        contar_nodos(hijo) for hijo in nodo.hijos
    )


def contar_hojas(nodo):
    """Cuenta las regiones que no se subdividen."""
    if nodo.es_hoja():
        return 1

    return sum(contar_hojas(hijo) for hijo in nodo.hijos)


def profundidad_arbol(nodo):
    """Calcula la profundidad maxima, contando la raiz como nivel 1."""
    if nodo.es_hoja():
        return 1

    return 1 + max(
        profundidad_arbol(hijo) for hijo in nodo.hijos
    )


def reconstruir_imagen(nodo, matriz):
    """Reconstruye la imagen pintando las regiones hoja."""
    if nodo.es_hoja():
        color = np.clip(nodo.color, 0, 255).astype(np.uint8)

        matriz[
            nodo.y:nodo.y + nodo.alto,
            nodo.x:nodo.x + nodo.ancho
        ] = color

        return

    for hijo in nodo.hijos:
        reconstruir_imagen(hijo, matriz)


def estimar_tamano_quadtree(nodo):
    """
    Estimacion simplificada del almacenamiento en bits.

    Por nodo: 1 bit para indicar hoja o subdivision.
    Por hoja: 24 bits para el color RGB.
    Por nodo: 128 bits para cuatro coordenadas/dimensiones
    representadas como cuatro enteros de 32 bits.

    No incluye cabeceras del archivo ni detalles del lenguaje.
    """
    bits = 1 + 128

    if nodo.es_hoja():
        bits += 24
    else:
        for hijo in nodo.hijos:
            bits += estimar_tamano_quadtree(hijo)

    return bits


def main():
    # Buscar imagenes compatibles
    extensiones = {".png", ".jpg", ".jpeg", ".bmp"}

    archivos = sorted(
        archivo for archivo in CARPETA_IMAGENES.iterdir()
        if archivo.suffix.lower() in extensiones
    )

    if not archivos:
        print("No hay imagenes en la carpeta 'imagenes'.")
        print("Coloca alli una imagen JPG o PNG.")
        return

    # Seleccionar la primera imagen encontrada
    ruta_imagen = archivos[0]
    imagen = Image.open(ruta_imagen).convert("RGB")
    original = np.array(imagen)

    alto, ancho, canales = original.shape
    tolerancia = 15

    print("=" * 45)
    print("PROYECTO QUADTREE")
    print("Compresion de imagenes con Divide y Venceras")
    print("=" * 45)

    print(f"Imagen: {ruta_imagen.name}")
    print(f"Dimensiones: {ancho} x {alto}")
    print(f"Pixeles: {ancho * alto}")
    print(f"Tolerancia: {tolerancia}")

    # Construir el arbol y medir su tiempo
    print("\nConstruyendo Quadtree...")
    inicio = time.perf_counter()

    arbol = construir_quadtree(
        original, 0, 0, ancho, alto, tolerancia
    )

    tiempo = time.perf_counter() - inicio

    # Reconstruir la imagen
    reconstruida = np.zeros_like(original)
    reconstruir_imagen(arbol, reconstruida)

    ruta_reconstruida = CARPETA_RESULTADOS / "reconstruida.png"
    Image.fromarray(reconstruida).save(ruta_reconstruida)

    # Calcular el error cuadratico medio
    diferencia = (
        original.astype(float) - reconstruida.astype(float)
    )
    mse = float(np.mean(diferencia ** 2))

    # Estimar almacenamiento
    # Imagen original RGB sin comprimir: 24 bits por pixel
    bits_originales = original.size * 8
    bits_quadtree = estimar_tamano_quadtree(arbol)

    razon_compresion = bits_originales / bits_quadtree
    porcentaje_reduccion = (
        (1 - bits_quadtree / bits_originales) * 100
    )

    # Calcular las metricas del arbol
    nodos = contar_nodos(arbol)
    hojas = contar_hojas(arbol)
    profundidad = profundidad_arbol(arbol)

    print("\n========== RESULTADOS ==========")
    print(f"Nodos totales: {nodos}")
    print(f"Nodos hoja: {hojas}")
    print(f"Profundidad maxima: {profundidad}")
    print(f"Tiempo de construccion: {tiempo:.4f} segundos")
    print(f"MSE de reconstruccion: {mse:.4f}")

    print("\n======= ALMACENAMIENTO =======")
    print(f"Imagen original: {bits_originales} bits")
    print(f"Quadtree estimado: {bits_quadtree} bits")
    print(f"Razon de compresion: {razon_compresion:.4f}")
    print(f"Reduccion estimada: {porcentaje_reduccion:.2f}%")

    if razon_compresion > 1:
        print("La estimacion indica reduccion de almacenamiento.")
    elif razon_compresion < 1:
        print("La estimacion indica aumento de almacenamiento.")
    else:
        print("Ambas representaciones tienen el mismo tamano estimado.")

    print(f"\nImagen reconstruida: {ruta_reconstruida}")

    # Guardar una comparacion visual lado a lado
    comparacion = Image.new(
        "RGB", (ancho * 2, alto), "white"
    )
    comparacion.paste(imagen, (0, 0))
    comparacion.paste(
        Image.fromarray(reconstruida), (ancho, 0)
    )

    ruta_comparacion = CARPETA_RESULTADOS / "comparacion.png"
    comparacion.save(ruta_comparacion)

    print(f"Comparacion visual: {ruta_comparacion}")
    print("\nProceso terminado correctamente.")


if __name__ == "__main__":
    main()
