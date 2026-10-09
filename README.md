# Compresión de imágenes mediante Quadtree

## Descripción

Este proyecto implementa un algoritmo de compresión aproximada de imágenes mediante una estructura Quadtree y la estrategia Divide y Vencerás.

El algoritmo divide una imagen en regiones más pequeñas cuando sus píxeles no cumplen el criterio de uniformidad establecido. Las regiones que cumplen el criterio se representan mediante hojas del árbol y se utilizan para reconstruir la imagen.

## Estructura del proyecto

- `main.py`: ejecución principal del proyecto.
- `quadtree.py`: implementación de la estructura Quadtree y sus operaciones.
- `experimentos.py`: ejecución de las pruebas experimentales.
- `graficas.py`: generación de gráficas a partir de los resultados.
- `imagenes/`: imágenes utilizadas en las pruebas.
- `resultados/`: resultados, imágenes reconstruidas, archivo CSV y gráficas.
- `requirements.txt`: dependencias necesarias.

## Requisitos

- Python 3.
- Pillow.
- NumPy.
- pandas.
- Matplotlib.

## Instalación

Abre una terminal en la carpeta principal del proyecto y ejecuta:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Para ejecutar el programa principal:

```bash
python main.py
```

Para realizar los experimentos:

```bash
python experimentos.py
```

Para generar las gráficas:

```bash
python graficas.py
```

## Resultados experimentales

Los resultados se guardan en `resultados/experimentos.csv`. El archivo contiene los registros de las pruebas realizadas con diferentes imágenes, tamaños y tolerancias.

Las gráficas permiten analizar el error de reconstrucción, el tiempo de procesamiento y la razón de compresión estimada.

## Observación

La razón de compresión calculada por el programa es una estimación basada en la representación del Quadtree. No debe interpretarse como una medición del tamaño de un archivo comprimido real, a menos que se implemente y mida también su codificación y almacenamiento.
