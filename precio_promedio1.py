def calcular_recompra_y_stop_loss_escalonado():
    print("=== Cálculo Optimizado de Recompra con Stop Loss Escalonado ===")
    
    # Datos de entrada
    precio_long = float(input("Ingrese el precio de la posición LONG: "))
    tokens_long = float(input("Ingrese la cantidad de tokens en la posición LONG: "))
    
    precio_short = float(input("Ingrese el precio de la posición SHORT: "))
    tokens_short = float(input("Ingrese la cantidad de tokens en la posición SHORT: "))
    
    precio_actual = float(input("Ingrese el precio actual: "))
    precio_objetivo = float(input("Ingrese el precio objetivo para el rebote: "))
    stop_loss_porcentajes = [float(p) / 100 for p in input("Ingrese 3 porcentajes de stop loss separados por comas (por ejemplo, 0.5, 1, 1.5): ").split(",")]

    # Mostrar datos iniciales ingresados
    print("\n=== Datos Iniciales ===")
    print(f"Precio LONG: {precio_long:.6f}, Tokens LONG: {tokens_long:.6f}")
    print(f"Precio SHORT: {precio_short:.6f}, Tokens SHORT: {tokens_short:.6f}")
    print(f"Precio Actual: {precio_actual:.6f}")
    print(f"Precio Objetivo: {precio_objetivo:.6f}")
    
    # Calcular PNL actual
    pnl_long_actual = tokens_long * (precio_actual - precio_long)
    pnl_short_actual = tokens_short * (precio_short - precio_actual)
    pnl_total_actual = pnl_long_actual + pnl_short_actual
    
    print(f"\nPNL actual basado en el precio actual:")
    print(f"PNL de la posición LONG: {pnl_long_actual:.6f}")
    print(f"PNL de la posición SHORT: {pnl_short_actual:.6f}")
    print(f"PNL total: {pnl_total_actual:.6f}")
    
    # Calcular tokens adicionales necesarios para promediar el precio actual al precio objetivo
    tokens_total = tokens_long + tokens_short
    nuevo_precio_promedio = (
        (tokens_long * precio_long + tokens_short * precio_short + tokens_total * precio_actual) 
        / (tokens_long + tokens_short + tokens_total)
    )
    
    tokens_recompra = tokens_total * abs(precio_objetivo - nuevo_precio_promedio) / (precio_objetivo - precio_actual)

    # Cálculo de stop loss escalonado
    tokens_por_nivel = tokens_recompra / len(stop_loss_porcentajes)
    pnl_perdidas_escalonadas = []
    for nivel, porcentaje in enumerate(stop_loss_porcentajes, 1):
        precio_stop = nuevo_precio_promedio * (1 - porcentaje)
        pnl_nivel = tokens_por_nivel * (precio_stop - nuevo_precio_promedio)
        pnl_total_contrario = pnl_long_actual + pnl_short_actual + pnl_nivel
        pnl_perdidas_escalonadas.append((nivel, precio_stop, pnl_nivel, pnl_total_contrario))
    
    # Mostrar resultados
    print("\n=== Resultados optimizados ===")
    print(f"Tokens adicionales necesarios para promediar: {tokens_recompra:.6f}")
    print(f"Nuevo precio promedio: {nuevo_precio_promedio:.6f}")
    print(f"PNL estimado en caso de rebote al precio objetivo: {pnl_total_actual + tokens_recompra * abs(precio_objetivo - precio_actual):.6f}")
    
    print("\n=== Stop Loss Escalonado ===")
    for nivel, precio_stop, pnl_nivel, pnl_total_contrario in pnl_perdidas_escalonadas:
        print(f"Nivel {nivel}:")
        print(f"  Precio Stop Loss: {precio_stop:.6f}")
        print(f"  Tokens asignados: {tokens_por_nivel:.6f}")
        print(f"  Pérdida en este nivel: {pnl_nivel:.6f}")
        print(f"  PNL Total Contrario: {pnl_total_contrario:.6f}")

# Ejecutar la función
calcular_recompra_y_stop_loss_escalonado()
