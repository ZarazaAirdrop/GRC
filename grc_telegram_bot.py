from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from docx import Document
from datetime import datetime

TOKEN = "7740133597:AAFyxdxfZ-Dkm3jz1RXSS89z9aCEU8dSkTc"  # Tu API Key

# Variables globales
datos = {}
estado = {}

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu Gestor de Riesgo Cripto.\nPor favor, indica si la recompra es para 'long' o 'short'."
    )
    estado[update.effective_user.id] = "tipo_recompra"

# Procesar mensajes
async def procesar_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text.strip().lower()

    # Flujo de recolección de datos
    if estado.get(user_id) == "tipo_recompra":
        if texto in ["long", "short"]:
            datos[user_id] = {"tipo_recompra": texto}
            estado[user_id] = "precio_long"
            await update.message.reply_text("Perfecto, ahora dime el precio LONG.")
        else:
            await update.message.reply_text("Por favor, indica 'long' o 'short'.")
    elif estado.get(user_id) == "precio_long":
        datos[user_id]["precio_long"] = float(texto)
        estado[user_id] = "tokens_long"
        await update.message.reply_text("Dime el valor para tokens long.")
    elif estado.get(user_id) == "tokens_long":
        datos[user_id]["tokens_long"] = float(texto)
        estado[user_id] = "precio_short"
        await update.message.reply_text("Dime el valor para precio short.")
    elif estado.get(user_id) == "precio_short":
        datos[user_id]["precio_short"] = float(texto)
        estado[user_id] = "tokens_short"
        await update.message.reply_text("Dime el valor para tokens short.")
    elif estado.get(user_id) == "tokens_short":
        datos[user_id]["tokens_short"] = float(texto)
        estado[user_id] = "precio_actual"
        await update.message.reply_text("Dime el valor para precio actual.")
    elif estado.get(user_id) == "precio_actual":
        datos[user_id]["precio_actual"] = float(texto)
        estado[user_id] = "precio_recompra"
        await update.message.reply_text("Dime el valor para precio recompra.")
    elif estado.get(user_id) == "precio_recompra":
        datos[user_id]["precio_recompra"] = float(texto)
        estado[user_id] = "tokens_recompra"
        await update.message.reply_text("Dime el valor para tokens recompra.")
    elif estado.get(user_id) == "tokens_recompra":
        datos[user_id]["tokens_recompra"] = float(texto)
        estado[user_id] = "capital_total"
        await update.message.reply_text("Dime el valor para capital total.")
    elif estado.get(user_id) == "capital_total":
        datos[user_id]["capital_total"] = float(texto)
        estado[user_id] = "capital_riesgo"
        await update.message.reply_text("Dime el valor para capital riesgo.")
    elif estado.get(user_id) == "capital_riesgo":
        datos[user_id]["capital_riesgo"] = float(texto)
        estado[user_id] = "niveles_stop_loss"
        await update.message.reply_text("Dime el valor para niveles stop loss.")
    elif estado.get(user_id) == "niveles_stop_loss":
        datos[user_id]["niveles_stop_loss"] = int(texto)
        estado[user_id] = "niveles_take_profit"
        await update.message.reply_text("Dime el valor para niveles take profit.")
    elif estado.get(user_id) == "niveles_take_profit":
        datos[user_id]["niveles_take_profit"] = int(texto)
        estado[user_id] = "porcentaje_take_profit"
        await update.message.reply_text("Dime el valor para porcentaje take profit.")
    elif estado.get(user_id) == "porcentaje_take_profit":
        datos[user_id]["porcentaje_take_profit"] = float(texto)
        estado[user_id] = None
        await calcular_resultados(update, datos[user_id])
    else:
        await update.message.reply_text("Algo salió mal. Intenta de nuevo con /start.")

async def calcular_resultados(update: Update, datos: dict):
    tipo_recompra = datos["tipo_recompra"]
    if tipo_recompra == "long":
        nuevo_precio = (
            (datos["tokens_long"] * datos["precio_long"] + datos["tokens_recompra"] * datos["precio_recompra"])
            / (datos["tokens_long"] + datos["tokens_recompra"])
        )
    elif tipo_recompra == "short":
        nuevo_precio = (
            (datos["tokens_short"] * datos["precio_short"] + datos["tokens_recompra"] * datos["precio_recompra"])
            / (datos["tokens_short"] + datos["tokens_recompra"])
        )
    else:
        nuevo_precio = 0  # Manejo de errores en caso de tipo de operación inválido


    niveles_stop_loss = calcular_stop_loss(datos, nuevo_precio, tipo_recompra)
    niveles_take_profit = calcular_take_profit(datos, nuevo_precio, tipo_recompra)

    crear_documento(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit)

    resultados = formatear_resultados(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit)
    await update.message.reply_text(resultados, parse_mode="Markdown")
    await update.message.reply_text("¡Cálculos realizados! Se generó un archivo Word con los resultados.")

def calcular_stop_loss(datos, nuevo_precio, tipo_recompra):
    niveles = datos["niveles_stop_loss"]
    tokens_recompra = datos["tokens_recompra"]

    # Porcentajes predeterminados para Stop Loss (puedes ajustarlos según tus necesidades)
    porcentajes = [0.4, 0.3, 0.2, 0.1, 0.0]
    porcentajes = porcentajes[:niveles]  # Ajustar al número de niveles configurado

    # Distribuir tokens basados en los porcentajes
    tokens_por_nivel = [tokens_recompra * p for p in porcentajes]

    factor = -1 if tipo_recompra == "long" else 1
    precio_base = datos["precio_recompra"] * (1 + 0.01 * factor)  # Margen del 1%

    return [
        {
            "Nivel": i + 1,
            "Precio": round(precio_base + factor * (0.01 * i * precio_base), 6),
            "Tokens": round(tokens_por_nivel[i], 6),
        }
        for i in range(niveles)
    ]

def calcular_take_profit(datos, nuevo_precio, tipo_recompra):
    niveles = datos["niveles_take_profit"]
    tokens_recompra = datos["tokens_recompra"]

    # Porcentajes predeterminados para Take Profit
    porcentajes = [0.2, 0.3, 0.5]
    porcentajes = porcentajes[:niveles]  # Ajustar al número de niveles configurado

    # Distribuir tokens basados en los porcentajes
    tokens_por_nivel = [tokens_recompra * p for p in porcentajes]

    porcentaje_tp = datos["porcentaje_take_profit"] / 100
    factor = 1 if tipo_recompra == "long" else -1

    return [
        {
            "Nivel": i + 1,
            "Precio": round(nuevo_precio + factor * (porcentaje_tp * (i + 1) * nuevo_precio), 6),
            "Tokens": round(tokens_por_nivel[i], 6),
        }
        for i in range(niveles)
    ]

# Crear documento
def crear_documento(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit):
    doc = Document()
    doc.add_heading("Gestor de Riesgo Cripto (GRC)", level=1)
    doc.add_heading("Datos Ingresados:", level=2)
    for clave, valor in datos.items():
        doc.add_paragraph(f"{clave.capitalize()}: {valor}")
    doc.add_heading("Resultados Calculados:", level=2)
    doc.add_paragraph(f"Nuevo Precio Promedio: {nuevo_precio:.6f}")
    doc.add_heading("Niveles de Stop Loss:", level=2)
    for nivel in niveles_stop_loss:
        doc.add_paragraph(f"Nivel {nivel['Nivel']}: Precio {nivel['Precio']:.6f}, Tokens {nivel['Tokens']:.6f}")
    doc.add_heading("Niveles de Take Profit:", level=2)
    for nivel in niveles_take_profit:
        doc.add_paragraph(f"Nivel {nivel['Nivel']}: Precio {nivel['Precio']:.6f}, Tokens {nivel['Tokens']:.6f}")
    nombre_archivo = f"Resultados/GRC_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(nombre_archivo)

# Formatear resultados para Telegram
def formatear_resultados(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit):
    resultados = "**Datos Ingresados:**\n"
    for clave, valor in datos.items():
        resultados += f"- {clave.capitalize()}: {valor}\n"
    resultados += f"\n**Nuevo Precio Promedio:** {nuevo_precio:.6f}\n\n"
    resultados += "**Niveles de Stop Loss:**\nNivel | Precio    | Tokens\n"
    for nivel in niveles_stop_loss:
        resultados += f"{nivel['Nivel']}     | {nivel['Precio']:.6f} | {nivel['Tokens']:.6f}\n"
    resultados += "\n**Niveles de Take Profit:**\nNivel | Precio    | Tokens\n"
    for nivel in niveles_take_profit:
        resultados += f"{nivel['Nivel']}     | {nivel['Precio']:.6f} | {nivel['Tokens']:.6f}\n"
    return resultados

# Configuración del bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_datos))

print("Bot en ejecución...")
app.run_polling()