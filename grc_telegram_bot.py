from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import os
import asyncio

# Obtener el token de la variable de entorno
TOKEN = os.getenv("TOKEN")

# Variables globales
datos = {}
estado = {}
usuarios_activos = set()

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    usuarios_activos.add(user_id)  # Activar el usuario
    await update.message.reply_text(
        "¡Hola! Soy tu Gestor de Riesgo Cripto.\nPor favor, indica si la recompra es para 'long' o 'short'."
    )
    estado[user_id] = "tipo_recompra"

# Procesar mensajes
async def procesar_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in usuarios_activos:
        await update.message.reply_text("¿Quieres iniciar el bot de gestión de riesgo GRC? Escribe `/start` para comenzar.")
        return

    texto = update.message.text.strip().lower().replace(",", ".")  # Reemplazar coma por punto

    try:
        # Lógica del bot
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
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}. Por favor, introduce un número válido.")
    except Exception as e:
        await update.message.reply_text("Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde.")

async def calcular_resultados(update: Update, datos: dict):
    # Aquí irían los cálculos del bot y el envío de resultados.
    # Mostrar al final:
    await update.message.reply_text(
        "¿Quieres seguir utilizando el bot? Escribe `/start` para continuar. "
        "Si no respondes, el bot se desconectará en 5 minutos."
    )
    await asyncio.sleep(300)  # Esperar 5 minutos
    if update.effective_user.id in usuarios_activos:
        usuarios_activos.remove(update.effective_user.id)
        await update.message.reply_text("El bot se ha desconectado. Escribe `/start` para volver a activarlo.")

# Configuración del bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_datos))

print("Bot en ejecución...")
app.run_polling()
