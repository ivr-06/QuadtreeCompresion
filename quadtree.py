
import numpy as np


class NodoQuadtree:
    """Representa una region de la imagen."""

    def __init__(self, x, y, ancho, alto, color=None):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.hijos = []

    def es_hoja(self):
        """Una hoja no tiene subdivisiones."""
        return len(self.hijos) == 0


def construir_quadtree(imagen, x, y, ancho, alto, tolerancia=15):
    """
    Construye el Quadtree recursivamente.

    imagen: matriz RGB de la imagen.
    x, y: coordenadas de la region.
    ancho, alto: dimensiones de la region.
    tolerancia: diferencia de color permitida.
    """

    # Obtener los pixeles de la region actual
    region = imagen[y:y + alto, x:x + ancho]

    # Calcular el color promedio de la region
    color_promedio = np.mean(region, axis=(0, 1))

    # Medir la mayor diferencia respecto al color promedio
    diferencia = np.max(
        np.abs(region.astype(float) - color_promedio)
    )

    # Caso base: region uniforme o de un solo pixel
    if diferencia <= tolerancia or (ancho == 1 and alto == 1):
        return NodoQuadtree(
            x, y, ancho, alto, color_promedio
        )

    # Dividir las dimensiones, incluyendo medidas impares
    mitad_ancho = ancho // 2
    mitad_alto = alto // 2

    divisiones = [
        (x, y, mitad_ancho, mitad_alto),
        (x + mitad_ancho, y, ancho - mitad_ancho, mitad_alto),
        (x, y + mitad_alto, mitad_ancho, alto - mitad_alto),
        (
            x + mitad_ancho,
            y + mitad_alto,
            ancho - mitad_ancho,
            alto - mitad_alto
        )
    ]

    # Crear el nodo padre
    nodo = NodoQuadtree(x, y, ancho, alto)

    # Resolver cada subregion recursivamente
    for nx, ny, nw, nh in divisiones:
        if nw > 0 and nh > 0:
            hijo = construir_quadtree(
                imagen, nx, ny, nw, nh, tolerancia
            )
            nodo.hijos.append(hijo)

    # Combinar las soluciones en el nodo padre
    return nodo
