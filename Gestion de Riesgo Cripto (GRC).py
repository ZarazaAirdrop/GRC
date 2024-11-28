def calcular_recompra_stop_loss():
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
        "Capital Riesgo (USD)": float(input("Ingrese el capital máximo a arriesgar por operación en USD: "))
    }

    # Extraer datos
    precio_long = datos_ingresados["Precio LONG"]
    tokens_long = datos_ingresados["Tokens LONG"]
    precio_recompra = datos_ingresados["Precio Recompra"]
    if precio_recompra == 0:  # Usar precio actual si no se proporciona un precio específico
        precio_recompra = datos_ingresados["Precio Actual"]
    tokens_recompra = datos_ingresados["Cantidad Tokens Recompra"]
    precio_actual = datos_ingresados["Precio Actual"]

    # Cálculos PNL
    pnl_long = (precio_actual - precio_long) * tokens_long
    pnl_short = 0  # Si se necesita incluir la posición short, se puede añadir aquí.
    pnl_total = pnl_long + pnl_short

    # Cálculo del nuevo precio promedio
    nuevo_precio_promedio = (
        (tokens_long * precio_long + tokens_recompra * precio_recompra) /
        (tokens_long + tokens_recompra)
    )

    # Cálculo de niveles de stop loss
    niveles_stop_loss = 3
    distancia_porcentaje = 0.5  # 0.5% de distancia entre niveles
    tokens_por_nivel = tokens_recompra / niveles_stop_loss
    stop_losses = []

    for nivel in range(1, niveles_stop_loss + 1):
        precio_stop = precio_recompra - (nivel * distancia_porcentaje / 100 * precio_recompra)
        perdida_nivel = (precio_stop - nuevo_precio_promedio) * tokens_por_nivel
        pnl_total_nivel = pnl_total + perdida_nivel
        stop_losses.append({
            "nivel": nivel,
            "precio_stop": precio_stop,
            "tokens_asignados": tokens_por_nivel,
            "perdida_nivel": perdida_nivel,
            "pnl_total_nivel": pnl_total_nivel
        })

    # Mostrar resultados en consola
    print("\n=== Resultados ===")
    print(f"PNL actual (USD):\n  PNL LONG: {pnl_long:.6f}\n  PNL TOTAL: {pnl_total:.6f}")
    print(f"\nTokens necesarios para promediar:\n  Tokens Recompra: {tokens_recompra:.6f}\n  Nuevo Precio Promedio: {nuevo_precio_promedio:.6f}")
    print("\nNiveles de Stop Loss:")
    for stop_loss in stop_losses:
        print(f"  Nivel {stop_loss['nivel']}:\n    Precio Stop: {stop_loss['precio_stop']:.6f}\n    Tokens Asignados: {stop_loss['tokens_asignados']:.6f}")
        print(f"    Pérdida Nivel: {stop_loss['perdida_nivel']:.6f}\n    PNL Total en Nivel: {stop_loss['pnl_total_nivel']:.6f}")

    # Guardar resultados en archivo de texto
    guardar_resultados_en_texto(datos_ingresados, pnl_long, pnl_short, pnl_total, tokens_recompra, nuevo_precio_promedio, stop_losses)

def guardar_resultados_en_texto(datos_ingresados, pnl_long, pnl_short, pnl_total, tokens_recompra, nuevo_precio_promedio, stop_losses):
    archivo = "resultados_grc.txt"
    with open(archivo, "w") as file:
        file.write("=== Gestor de Riesgo Cripto (GRC) ===\n")
        file.write("-" * 50 + "\n")
        
        # Datos ingresados
        file.write("DATOS INGRESADOS:\n")
        for clave, valor in datos_ingresados.items():
            file.write(f"  {clave}: {valor}\n")
        file.write("-" * 50 + "\n")
        
        # Resumen PNL
        file.write("RESUMEN PNL ACTUAL (USD):\n")
        file.write(f"  PNL LONG: {pnl_long:.6f}\n")
        file.write(f"  PNL TOTAL: {pnl_total:.6f}\n")
        file.write("-" * 50 + "\n")
        
        # Tokens necesarios para promediar
        file.write("TOKENS NECESARIOS PARA PROMEDIAR:\n")
        file.write(f"  Tokens Recompra: {tokens_recompra:.6f}\n")
        file.write(f"  Nuevo Precio Promedio: {nuevo_precio_promedio:.6f}\n")
        file.write("-" * 50 + "\n")
        
        # Niveles de Stop Loss
        file.write("NIVELES DE STOP LOSS:\n")
        for stop_loss in stop_losses:
            file.write(f"  Nivel {stop_loss['nivel']}:\n")
            file.write(f"    Precio Stop: {stop_loss['precio_stop']:.6f}\n")
            file.write(f"    Tokens Asignados: {stop_loss['tokens_asignados']:.6f}\n")
            file.write(f"    Pérdida Nivel: {stop_loss['perdida_nivel']:.6f}\n")
            file.write(f"    PNL Total en Nivel: {stop_loss['pnl_total_nivel']:.6f}\n")
            file.write("-" * 50 + "\n")

    print(f"\nResultados exportados a '{archivo}' para su visualización.")

# Ejecución directa del programa
calcular_recompra_stop_loss()
