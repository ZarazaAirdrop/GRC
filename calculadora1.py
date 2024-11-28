def calculadora_trading():
    print("=== Calculadora de Trading para Método de Cobertura ===")
    
    # Preguntar tipo de posición inicial
    tipo_posicion = input("¿La posición inicial es 'long' o 'short'? (Ingrese 'long' o 'short'): ").strip().lower()
    if tipo_posicion not in ['long', 'short']:
        print("Tipo de posición inválido. Solo se acepta 'long' o 'short'.")
        return
    
    # Datos iniciales de la posición
    precio_inicial = float(input("Ingrese el precio de entrada de la posición inicial: "))
    tokens_iniciales = float(input("Ingrese la cantidad de tokens para la posición inicial: "))
    
    # Configuración de la cobertura
    porcentaje_movimiento = float(input("Ingrese el porcentaje de movimiento para activar la cobertura (por ejemplo, 3 para 3%): ")) / 100
    incremento_tokens = float(input("Ingrese el porcentaje de incremento en la cobertura (por ejemplo, 50 para 50%): ")) / 100
    pnl_parcial_porcentaje = float(input("Ingrese el porcentaje del PNL para tomar ganancias (por ejemplo, 25 para 25%): ")) / 100
    
    pnl_total = 0  # Inicializar el PNL total

    while True:
        print("\n--- Nuevo ciclo de cálculo ---")
        
        # Calcular el precio objetivo según el tipo de posición
        if tipo_posicion == 'long':
            precio_objetivo = precio_inicial * (1 + porcentaje_movimiento)
            print(f"Precio objetivo para cobertura (subida de {porcentaje_movimiento*100:.2f}%): {precio_objetivo:.2f}")
        else:  # Short
            precio_objetivo = precio_inicial * (1 - porcentaje_movimiento)
            print(f"Precio objetivo para cobertura (bajada de {porcentaje_movimiento*100:.2f}%): {precio_objetivo:.2f}")
        
        # Datos de la cobertura
        tokens_cobertura = tokens_iniciales * (1 + incremento_tokens)
        print(f"Cantidad de tokens para la cobertura: {tokens_cobertura:.2f}")
        
        # Preguntar el precio actual
        precio_actual = float(input("Ingrese el precio actual (o -1 para salir): "))
        if precio_actual == -1:
            break
        
        # Calcular si la cobertura se activa
        cobertura_activada = (precio_actual >= precio_objetivo if tipo_posicion == 'long' else precio_actual <= precio_objetivo)
        if cobertura_activada:
            print("¡Cobertura activada!")
            
            # Calcular el PNL parcial
            if tipo_posicion == 'long':
                pnl_parcial = pnl_parcial_porcentaje * tokens_cobertura * (precio_actual - precio_inicial)
            else:  # Short
                pnl_parcial = pnl_parcial_porcentaje * tokens_cobertura * (precio_inicial - precio_actual)
            
            pnl_total += pnl_parcial
            print(f"PNL parcial obtenido (tomado {pnl_parcial_porcentaje*100:.2f}%): {pnl_parcial:.2f}")
            print(f"PNL total acumulado: {pnl_total:.2f}")
            
            # Ajustar tokens y preparar para el próximo ciclo
            tokens_iniciales += tokens_cobertura * (1 - pnl_parcial_porcentaje)
            precio_inicial = precio_actual
            print(f"Nueva cantidad de tokens acumulados: {tokens_iniciales:.2f}")
        else:
            print("La cobertura no se activa en este ciclo.")

    print("\nEstrategia finalizada. ¡Éxitos en tu trading!").