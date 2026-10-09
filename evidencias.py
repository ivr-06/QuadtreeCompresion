from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from quadtree import construir_quadtree
from experimentos import (
    reconstruir, contar_nodos, contar_hojas,
    profundidad_arbol, estimar_bits
)

CARPETA_IMAGENES = Path("imagenes")
CARPETA_RESULTADOS = Path("resultados")
CARPETA_RESULTADOS.mkdir(exist_ok=True)

# Una evidencia por cada tipo de imagen. Las tres se procesan a 256x256.
CASOS = [
    ("Fotografia.jpg", 5, "Evidencia 1 - Fotografía con detalles"),
    ("Geometria.png", 15, "Evidencia 2 - Figuras geométricas"),
    ("Paisaje.jpg", 30, "Evidencia 3 - Paisaje con variación de color"),
]

def cargar_fuente(tamano):
    try:
        return ImageFont.truetype("arial.ttf", tamano)
    except OSError:
        return ImageFont.load_default()

def crear_evidencia(nombre, tolerancia, titulo):
    ruta = CARPETA_IMAGENES / nombre
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Comprueba que el archivo exista en la carpeta imagenes."
        )

    original_img = Image.open(ruta).convert("RGB").resize((256, 256))
    original = np.array(original_img)
    alto, ancho, _ = original.shape

    inicio = time.perf_counter()
    arbol = construir_quadtree(original, 0, 0, ancho, alto, tolerancia)
    tiempo = time.perf_counter() - inicio

    reconstruida = np.zeros_like(original)
    reconstruir(arbol, reconstruida)

    mse = float(np.mean((original.astype(float) - reconstruida.astype(float)) ** 2))
    bits_originales = original.size * 8
    bits_quadtree = estimar_bits(arbol)
    razon = bits_originales / bits_quadtree
    nodos = contar_nodos(arbol)
    hojas = contar_hojas(arbol)
    profundidad = profundidad_arbol(arbol)

    # Panel legible: imagen original, reconstrucción y métricas/configuración.
    ancho_panel, alto_panel = 900, 475
    panel = Image.new("RGB", (ancho_panel, alto_panel), "white")
    draw = ImageDraw.Draw(panel)
    fuente_titulo = cargar_fuente(22)
    fuente_sub = cargar_fuente(15)
    fuente_texto = cargar_fuente(17)

    draw.text((24, 18), titulo, fill="black", font=fuente_titulo)
    draw.text((24, 55), f"Archivo: {nombre} | Tamaño de prueba: {ancho}x{alto} | Tolerancia: {tolerancia}",
              fill="black", font=fuente_sub)

    # Las dos imágenes se muestran a tamaño legible.
    original_img = original_img.resize((350, 350))
    reconstruida_img = Image.fromarray(reconstruida).resize((350, 350))
    panel.paste(original_img, (55, 95))
    panel.paste(reconstruida_img, (495, 95))
    draw.text((55, 75), "Imagen original", fill="black", font=fuente_sub)
    draw.text((495, 75), "Imagen reconstruida", fill="black", font=fuente_sub)

    resumen = [
        f"Nodos: {nodos}    Hojas: {hojas}    Profundidad: {profundidad}",
        f"Tiempo de construcción: {tiempo:.4f} s    MSE: {mse:.4f}",
        f"Razón de compresión estimada: {razon:.4f}",
        "Nota: la razón de compresión es una estimación de bits, no el tamaño real de un archivo codificado."
    ]
    y = 455 - 4 * 22
    for linea in resumen:
        draw.text((24, y), linea, fill="black", font=fuente_texto if y < 445 else fuente_sub)
        y += 22

    salida = CARPETA_RESULTADOS / f"evidencia_{nombre.rsplit('.', 1)[0].lower()}.png"
    panel.save(salida)
    print(f"Guardada: {salida}")
    print(f"  Configuración: {ancho}x{alto}, tolerancia={tolerancia}")
    print(f"  Nodos={nodos}, hojas={hojas}, profundidad={profundidad}")
    print(f"  Tiempo={tiempo:.4f}s, MSE={mse:.4f}, razón estimada={razon:.4f}")

def main():
    for nombre, tolerancia, titulo in CASOS:
        crear_evidencia(nombre, tolerancia, titulo)
    print("\\nListo. Revisa la carpeta resultados: se crearon tres evidencias PNG.")

if __name__ == "__main__":
    main()
