import discord
from discord.ext import commands
import openpyxl
from keep_alive import keep_alive

# ---------- Настройки ----------
TOKEN = ""  # Добавь через Replit Secrets: DISCORD_TOKEN
OWNER_ID = 810897749817819136  # Твой Discord ID
EXCEL_FILE = "database.xlsx"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# ---------- База данных ----------
try:
    wb = openpyxl.load_workbook(EXCEL_FILE)
    sheet = wb.active
except:
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["User ID", "Name"])
    wb.save(EXCEL_FILE)

def add_user_to_db(user):
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0] == user.id:
            return False  # уже есть
    sheet.append([user.id, str(user)])
    wb.save(EXCEL_FILE)
    return True

# ---------- События ----------
@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен!")
    print(f"Синхронизировано {len(bot.commands)} команд")
    
@bot.event
async def on_command(ctx):
    added = add_user_to_db(ctx.author)
    if added:
        print(f"Добавлен новый пользователь: {ctx.author}")

# ---------- Команды ----------
@bot.slash_command(description="Пинг бота")
async def ping(ctx):
    await ctx.respond(f"Pong! 🏓")

@bot.slash_command(description="Показать базу данных (только владелец)")
async def db(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.respond("❌ Доступ запрещен")
        return
    data = ""
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data += f"{row[0]} - {row[1]}\n"
    if data == "":
        data = "База пустая"
    await ctx.respond(f"```{data}```")

# ---------- Запуск ----------
keep_alive()  # держим бота живым на Replit
bot.run(TOKEN)


