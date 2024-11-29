from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from docx import Document
from datetime import datetime
import os
import asyncio

TOKEN = os.getenv("TOKEN")

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
    await shutdown_bot()

async def shutdown_bot():
    """Cierra el bot después de ejecutar los cálculos."""
    await asyncio.sleep(2)  # Esperar un momento antes de desconectar
    os._exit(0)

def calcular_stop_loss(datos, nuevo_precio, tipo_recompra):
    # Función existente para calcular niveles de Stop Loss
    pass

def calcular_take_profit(datos, nuevo_precio, tipo_recompra):
    # Función existente para calcular niveles de Take Profit
    pass

def crear_documento(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit):
    # Función existente para generar un documento
    pass

def formatear_resultados(datos, nuevo_precio, niveles_stop_loss, niveles_take_profit):
    # Función existente para formatear resultados
    pass

# Configuración del bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_datos))

print("Bot en ejecución...")
app.run_polling()
