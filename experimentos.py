
from pathlib import Path
import csv
import time

import numpy as np
from PIL import Image

from quadtree import construir_quadtree


CARPETA_IMAGENES = Path("imagenes")
CARPETA_RESULTADOS = Path("resultados")
CARPETA_RESULTADOS.mkdir(exist_ok=True)


def contar_nodos(nodo):
    return 1 + sum(contar_nodos(hijo) for hijo in nodo.hijos)


def contar_hojas(nodo):
    if nodo.es_hoja():
        return 1
    return sum(contar_hojas(hijo) for hijo in nodo.hijos)


def profundidad_arbol(nodo):
    if nodo.es_hoja():
        return 1
    return 1 + max(profundidad_arbol(hijo) for hijo in nodo.hijos)


def reconstruir(nodo, matriz):
    if nodo.es_hoja():
        color = np.clip(nodo.color, 0, 255).astype(np.uint8)
        matriz[
            nodo.y:nodo.y + nodo.alto,
            nodo.x:nodo.x + nodo.ancho
        ] = color
        return

    for hijo in nodo.hijos:
        reconstruir(hijo, matriz)


def estimar_bits(nodo):
    # Modelo simplificado: 129 bits por nodo y 24 bits por hoja
    bits = 129

    if nodo.es_hoja():
        bits += 24
    else:
        for hijo in nodo.hijos:
            bits += estimar_bits(hijo)

    return bits


def ejecutar_experimentos():
    extensiones = {".jpg", ".jpeg", ".png", ".bmp"}

    imagenes = sorted(
        archivo for archivo in CARPETA_IMAGENES.iterdir()
        if archivo.suffix.lower() in extensiones
    )

    if not imagenes:
        print("Agrega al menos una imagen en la carpeta imagenes.")
        return

    # Tres tolerancias para comparar calidad y almacenamiento
    tolerancias = [5, 15, 30]
    resultados = []

    for ruta in imagenes:
        original_img = Image.open(ruta).convert("RGB")

        # Pruebas a tres tamaños
        for lado in [64, 128, 256]:
            imagen = original_img.resize((lado, lado))
            original = np.array(imagen)
            alto, ancho, _ = original.shape

            for tolerancia in tolerancias:
                inicio = time.perf_counter()

                arbol = construir_quadtree(
                    original, 0, 0, ancho, alto, tolerancia
                )

                tiempo = time.perf_counter() - inicio

                reconstruida = np.zeros_like(original)
                reconstruir(arbol, reconstruida)

                mse = float(np.mean(
                    (original.astype(float) -
                     reconstruida.astype(float)) ** 2
                ))

                bits_originales = original.size * 8
                bits_arbol = estimar_bits(arbol)

                razon = bits_originales / bits_arbol

                resultados.append({
                    "imagen": ruta.name,
                    "ancho": ancho,
                    "alto": alto,
                    "tolerancia": tolerancia,
                    "nodos": contar_nodos(arbol),
                    "hojas": contar_hojas(arbol),
                    "profundidad": profundidad_arbol(arbol),
                    "tiempo_segundos": round(tiempo, 6),
                    "mse": round(mse, 4),
                    "bits_originales": bits_originales,
                    "bits_quadtree_estimados": bits_arbol,
                    "razon_compresion_estimada": round(razon, 4)
                })

                print(
                    f"{ruta.name} | {lado}x{lado} | "
                    f"tolerancia={tolerancia} | "
                    f"MSE={mse:.2f} | "
                    f"tiempo={tiempo:.4f}s"
                )

    archivo_csv = CARPETA_RESULTADOS / "experimentos.csv"

    with open(archivo_csv, "w", newline="", encoding="utf-8-sig") as archivo:
        columnas = resultados[0].keys()
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"\nExperimentos terminados: {len(resultados)}")
    print(f"Resultados guardados en: {archivo_csv}")


if __name__ == "__main__":
    ejecutar_experimentos()
