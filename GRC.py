import json
from prettytable import PrettyTable
import os

def calcular_gestión():
    print("=== Ingresá los datos necesarios para el cálculo ===")

    # Solicitar datos iniciales
    datos_ingresados = {
        "Precio LONG": float(input("Ingrese el precio de la posición LONG: ")),
        "Tokens LONG": float(input("Ingrese la cantidad de tokens en LONG: ")),
        "Precio SHORT": float(input("Ingrese el precio de la posición SHORT: ")),
        "Tokens SHORT": float(input("Ingrese la cantidad de tokens en SHORT: ")),
        "Precio Actual": float(input("Ingrese el precio actual del token: ")),
        "Precio Recompra": float(input("Ingrese el precio esperado para la recompra (o 0 si es el precio actual): ")),
        "Cantidad Tokens Recompra": float(input("Ingrese la cantidad de tokens para la recompra: ")),
        "Capital Total (USD)": float(input("Ingrese el capital total disponible en USD: ")),
        "Capital Riesgo (USD)": float(input("Ingrese el capital máximo a arriesgar por operación en USD: ")),
        "Niveles de Stop Loss": int(input("Ingrese la cantidad de niveles de stop loss: ")),
        "Niveles de Take Profit": int(input("Ingrese la cantidad de niveles de take profit: ")),
        "Porcentaje de Take Profit": float(input("Ingrese el porcentaje de ganancia por nivel de take profit (%): "))
    }

    # Calcular nuevo precio promedio
    precio_long = datos_ingresados["Precio LONG"]
    tokens_long = datos_ingresados["Tokens LONG"]
    precio_recompra = datos_ingresados["Precio Recompra"] or datos_ingresados["Precio Actual"]
    tokens_recompra = datos_ingresados["Cantidad Tokens Recompra"]
    nuevo_precio_promedio = (
        (tokens_long * precio_long + tokens_recompra * precio_recompra) /
        (tokens_long + tokens_recompra)
    )

    # Cálculo de niveles de stop loss
    niveles_stop_loss = datos_ingresados["Niveles de Stop Loss"]
    tokens_por_stop = tokens_recompra / niveles_stop_loss
    distancia_stop = 0.5 / 100  # 0.5% por nivel
    stop_losses = []

    for i in range(1, niveles_stop_loss + 1):
        precio_stop = precio_recompra - (i * distancia_stop * precio_recompra)
        pérdida_nivel = (precio_stop - nuevo_precio_promedio) * tokens_por_stop
        stop_losses.append({
            "Nivel": i,
            "Precio": precio_stop,
            "Tokens": tokens_por_stop,
            "Resultado": pérdida_nivel
        })

    # Cálculo de niveles de take profit
    niveles_take_profit = datos_ingresados["Niveles de Take Profit"]
    tokens_por_tp = tokens_recompra / niveles_take_profit
    porcentaje_tp = datos_ingresados["Porcentaje de Take Profit"] / 100
    take_profits = []

    for i in range(1, niveles_take_profit + 1):
        precio_tp = nuevo_precio_promedio + (i * porcentaje_tp * nuevo_precio_promedio)
        ganancia_nivel = (precio_tp - nuevo_precio_promedio) * tokens_por_tp
        take_profits.append({
            "Nivel": i,
            "Precio": precio_tp,
            "Tokens": tokens_por_tp,
            "Resultado": ganancia_nivel
        })

    # Exportar datos a archivo JSON
    datos_exportados = {
        "Datos Ingresados": datos_ingresados,
        "Nuevo Precio Promedio": nuevo_precio_promedio,
        "Niveles de Stop Loss": stop_losses,
        "Niveles de Take Profit": take_profits
    }

    with open("datos_grc.json", "w") as archivo_json:
        json.dump(datos_exportados, archivo_json, indent=4)

    print("\nDatos calculados y exportados a 'datos_grc.json'. Ejecuta 'grc_docx.py' para generar el archivo Word.")

# Ejecutar el programa
calcular_gestión()
# Llamar al script que genera el documento Word
os.system('python grc_docx.py')