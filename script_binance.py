from binance.client import Client
from collections import defaultdict

# Conexión a Binance
api_key = "8Uxhi4946OhilSSBii34lRo7cx2wnN5OYVIqKwLLJdIiTVui7EniIU6RbLtDzPci"
api_secret = "n2UFKCiY6wOvbuw1SCofAVeeNYYiTWrQkRbxclzbJ4bmObRbvvaG6m0emflIUlho"
client = Client(api_key, api_secret)

# Función principal
def analizar_ordenes_binance():
    print("=== Conexión a Binance y análisis de mercado ===")
    par = input("Ingrese el par de trading (por ejemplo, BTCUSDT): ").strip().upper()
    
    # Obtener precio actual
    ticker = client.get_ticker(symbol=par)
    precio_actual = float(ticker['lastPrice'])
    print(f"\nPrecio actual de {par}: {precio_actual:.6f}")
    
    # Obtener libro de órdenes
    profundidad = client.get_order_book(symbol=par, limit=500)
    bids = profundidad['bids']  # Compras
    asks = profundidad['asks']  # Ventas

    # Rango de ±10% desde el precio actual
    rango_min = precio_actual * 0.9
    rango_max = precio_actual * 1.1

    def procesar_ordenes(ordenes, tipo):
        # Filtrar órdenes dentro del rango
        ordenes_filtradas = [
            (float(precio), float(cantidad))
            for precio, cantidad in ordenes
            if rango_min <= float(precio) <= rango_max
        ]
        
        # Agrupar en intervalos de 2%
        intervalos = defaultdict(list)
        for precio, cantidad in ordenes_filtradas:
            intervalo = round(((float(precio) - rango_min) / (rango_max - rango_min)) * 10) // 2
            intervalos[intervalo].append((precio, cantidad))
        
        # Calcular las 5 mayores acumulaciones por intervalo
        acumulaciones = {}
        for intervalo, ordenes in intervalos.items():
            mayores_acumulaciones = sorted(ordenes, key=lambda x: x[1], reverse=True)[:5]
            acumulaciones[intervalo] = mayores_acumulaciones
        
        return acumulaciones

    # Procesar compras y ventas
    print("\nTop acumulaciones en un rango de ±10% desde el precio actual:\n")
    print("=== Compras ===")
    acumulaciones_bids = procesar_ordenes(bids, "Compras")
    for intervalo, datos in acumulaciones_bids.items():
        print(f"\nIntervalo {(intervalo * 2):.1f}% - {(intervalo * 2 + 2):.1f}%:")
        for precio, cantidad in datos:
            print(f"Precio: {precio:.6f}, Cantidad: {cantidad:.6f}")
    
    print("\n=== Ventas ===")
    acumulaciones_asks = procesar_ordenes(asks, "Ventas")
    for intervalo, datos in acumulaciones_asks.items():
        print(f"\nIntervalo {(intervalo * 2):.1f}% - {(intervalo * 2 + 2):.1f}%:")
        for precio, cantidad in datos:
            print(f"Precio: {precio:.6f}, Cantidad: {cantidad:.6f}")

# Ejecutar el análisis
analizar_ordenes_binance()
