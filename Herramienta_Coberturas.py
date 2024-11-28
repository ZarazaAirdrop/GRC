from binance.client import Client

# === Configuración inicial ===
API_KEY = "8Uxhi4946OhilSSBii34lRo7cx2wnN5OYVIqKwLLJdIiTVui7EniIU6RbLtDzPci,"
API_SECRET = "n2UFKCiY6wOvbuw1SCofAVeeNYYiTWrQkRbxclzbJ4bmObRbvvaG6m0emflIUlho"

# Conexión a Binance
client = Client(API_KEY, API_SECRET)

def obtener_precio_actual(par):
    """Obtiene el precio actual de un par en Binance."""
    try:
        ticker = client.get_ticker(symbol=par)
        return float(ticker['lastPrice'])
    except Exception as e:
        print(f"Error al obtener precio actual: {e}")
        return None

def calcular_recompra_y_stop_loss(par):
    """Calcula la recompra y los stop loss escalonados."""
    print(f"\n=== Cálculo Optimizado para {par} ===")
    
    # Obtener precio actual automáticamente
    precio_actual = obtener_precio_actual(par)
    if precio_actual is None:
        print("No se pudo obtener el precio actual. Intente nuevamente.")
        return
    
    print(f"Precio actual: {precio_actual:.6f}")
    
    try:
        # Entrada de datos
        precio_long = float(input("Ingrese el precio de la posición LONG: "))
        tokens_long = float(input("Ingrese la cantidad de tokens en la posición LONG: "))
        
        precio_short = float(input("Ingrese el precio de la posición SHORT: "))
        tokens_short = float(input("Ingrese la cantidad de tokens en la posición SHORT: "))
        
        # Gestión de capital
        capital_total = float(input("Ingrese su capital total disponible en USD: "))
        porcentaje_riesgo = float(input("Ingrese el porcentaje de capital a arriesgar por operación (por ejemplo, 2): ")) / 100
        capital_riesgo = capital_total * porcentaje_riesgo
        
        # Preguntar sobre el contexto de rebote
        contexto = input("¿El rebote esperado es sobre la posición LONG o SHORT? (L/S): ").strip().upper()
        if contexto not in ["L", "S"]:
            print("Entrada inválida. Debe ingresar 'L' o 'S'.")
            return  # Terminar si la entrada no es válida
        
        precio_objetivo = float(input("Ingrese el precio objetivo para el rebote: "))
        stop_loss_porcentajes = [float(p) / 100 for p in input("Ingrese porcentajes de stop loss separados por comas (por ejemplo, 0.5, 1, 1.5): ").split(",")]
        
        # Mostrar datos iniciales
        print("\n=== Datos Iniciales ===")
        print(f"Precio LONG: {precio_long:.6f}, Tokens LONG: {tokens_long:.6f}")
        print(f"Precio SHORT: {precio_short:.6f}, Tokens SHORT: {tokens_short:.6f}")
        print(f"Precio Actual: {precio_actual:.6f}")
        print(f"Precio Objetivo: {precio_objetivo:.6f}")
        print(f"Capital Total: {capital_total:.2f} USD, Capital en Riesgo: {capital_riesgo:.2f} USD")
        
        # Calcular PNL actual
        pnl_long_actual = tokens_long * (precio_actual - precio_long)
        pnl_short_actual = tokens_short * (precio_short - precio_actual)
        pnl_total_actual = pnl_long_actual + pnl_short_actual
        
        print(f"\nPNL actual basado en el precio actual:")
        print(f"PNL de la posición LONG: {pnl_long_actual:.6f}")
        print(f"PNL de la posición SHORT: {pnl_short_actual:.6f}")
        print(f"PNL total: {pnl_total_actual:.6f}")
        
        # Calcular tokens adicionales necesarios para promediar
        tokens_recompra = (tokens_long + tokens_short) * abs(precio_objetivo - precio_actual) / abs(precio_actual - (precio_short if contexto == "S" else precio_long))
        nuevo_precio_promedio = (tokens_short * precio_short + tokens_recompra * precio_actual) / (tokens_short + tokens_recompra)
        
        # Stop loss escalonado
        tokens_por_nivel = tokens_recompra / len(stop_loss_porcentajes)
        riesgo_por_nivel = capital_riesgo / len(stop_loss_porcentajes)
        
        print("\n=== Resultados optimizados ===")
        print(f"Tokens adicionales necesarios para promediar: {tokens_recompra:.6f}")
        print(f"Nuevo precio promedio: {nuevo_precio_promedio:.6f}")
        
        print("\n=== Stop Loss Escalonado ===")
        for nivel, porcentaje in enumerate(stop_loss_porcentajes, 1):
            precio_stop = nuevo_precio_promedio * (1 - porcentaje)
            pnl_stop_loss = tokens_por_nivel * (precio_stop - nuevo_precio_promedio)
            pnl_total_contrario = pnl_total_actual + pnl_stop_loss
            perdida_nivel = min(abs(pnl_stop_loss), riesgo_por_nivel)
            
            print(f"Nivel {nivel}:")
            print(f"  Precio Stop Loss: {precio_stop:.6f}")
            print(f"  Tokens asignados: {tokens_por_nivel:.6f}")
            print(f"  Pérdida en este nivel: {pnl_stop_loss:.6f}")
            print(f"  Pérdida Ajustada (Gestión de Capital): {perdida_nivel:.6f}")
            print(f"  PNL Total Contrario: {pnl_total_contrario:.6f}")
    except ValueError as e:
        print(f"Error en la entrada de datos: {e}. Intente nuevamente.")

# === Menú Principal ===
def menu_principal():
    while True:
        print("\n=== Herramienta de Gestión de Trading ===")
        print("1. Calcular recompra y stop loss escalonado")
        print("2. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            par = input("Ingrese el par de trading (por ejemplo, BTCUSDT): ").upper()
            calcular_recompra_y_stop_loss(par)
        elif opcion == "2":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar menú principal
menu_principal()
