
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CARPETA_RESULTADOS = Path("resultados")
archivo_csv = CARPETA_RESULTADOS / "experimentos.csv"

if not archivo_csv.exists():
    print("No se encontro experimentos.csv.")
    print("Ejecuta primero: python experimentos.py")
    raise SystemExit

datos = pd.read_csv(archivo_csv)

# Grafica 1: error MSE segun tolerancia
plt.figure(figsize=(8, 5))

for tamano, grupo in datos.groupby("ancho"):
    promedio = grupo.groupby("tolerancia")["mse"].mean()
    plt.plot(
        promedio.index,
        promedio.values,
        marker="o",
        label=f"{tamano} x {tamano}"
    )

plt.title("Error MSE segun tolerancia")
plt.xlabel("Tolerancia")
plt.ylabel("MSE")
plt.legend(title="Tamano de imagen")
plt.grid(True)
plt.tight_layout()
plt.savefig(CARPETA_RESULTADOS / "grafica_mse.png")
plt.close()


# Grafica 2: tiempo segun tamano
plt.figure(figsize=(8, 5))

for tolerancia, grupo in datos.groupby("tolerancia"):
    promedio = grupo.groupby("ancho")["tiempo_segundos"].mean()
    plt.plot(
        promedio.index,
        promedio.values,
        marker="o",
        label=f"Tolerancia {tolerancia}"
    )

plt.title("Tiempo de construccion del Quadtree")
plt.xlabel("Ancho de imagen (pixeles)")
plt.ylabel("Tiempo (segundos)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(CARPETA_RESULTADOS / "grafica_tiempo.png")
plt.close()


# Grafica 3: razon de compresion estimada
columna = "razon_compresion_estimada"

plt.figure(figsize=(8, 5))

for tamano, grupo in datos.groupby("ancho"):
    promedio = grupo.groupby("tolerancia")[columna].mean()
    plt.plot(
        promedio.index,
        promedio.values,
        marker="o",
        label=f"{tamano} x {tamano}"
    )

plt.title("Razon de compresion estimada")
plt.xlabel("Tolerancia")
plt.ylabel("Razon de compresion")
plt.legend(title="Tamano de imagen")
plt.grid(True)
plt.tight_layout()
plt.savefig(CARPETA_RESULTADOS / "grafica_compresion.png")
plt.close()

print("Graficas creadas correctamente:")
print("- resultados/grafica_mse.png")
print("- resultados/grafica_tiempo.png")
print("- resultados/grafica_compresion.png")
