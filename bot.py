import psutil
import telebot

TOKEN   = 'write yout bot token here' # sesuaikan dengan token bot masing-masing
bot     = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, "Halo, selamat datang di monitoring server bot\nSilahkan ketikan perintah berikut :\n\n/start - untuk memulai bot\n/server - untuk melihat penggunaan server\n/getid - untuk melihat id telegram\n\nTerima Kasih")

@bot.message_handler(commands=['getid'])
def command_getid(message):
    chatid = message.chat.id
    bot.reply_to(message, f"ID Telegram kamu : `{chatid}`", parse_mode="Markdown")
    
@bot.message_handler(commands=['server'])
def command_server(message):
    memory  = get_memory()
    ssd     = get_disk()
    cpu     = get_cpu()
    text = f"`Monitoring Server BOT\n\n"
    text += f"CPU : {cpu}%\n"
    text += f"MEM : {memory['used']:,}/{memory['total']:,} GB ({memory['percent']}%)\n"
    text += f"SSD : {ssd['used']:,}/{ssd['total']:,} GB ({ssd['percent']}%)\n"
    text += f"FRE : {ssd['free']:,} GB\n"
    text += "---\n"
    text += print_bar("CPU : ", cpu) + "\n"
    text += print_bar("MEM : ", memory['percent']) + "\n"
    text += print_bar("SSD : ", ssd['percent']) + "\n"
    text += "\n"
    text += "Terima Kasih`"
    bot.reply_to(message, text, parse_mode="Markdown")

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_memory():
    mem = psutil.virtual_memory()
    return {
        "total"     : int(round(mem.total/1024/1024/1024,0)),
        "used"      : int(round(mem.used/1024/1024/1024,0)),
        "available" : int(round(mem.available/1024/1024/1024,0)),
        "percent"   : mem.percent
    }
    
def get_disk():
    disk = psutil.disk_usage("/")
    return {
        "total"     : int(round(disk.total/1024/1024/1024,0)),
        "used"      : int(round(disk.used/1024/1024/1024,0)),
        "free"      : int(round(disk.free/1024/1024/1024,0)),
        "percent"   : disk.percent
    }

def print_bar(label = "", percent = 0):
    bar         = "█"
    bar_empty   = "░"
    text = label
    for d in range(10):
        if d <= int(percent/10):
            text += bar
        else:
            text += bar_empty
    text += f" ({percent}%)"
    return text

bot.infinity_polling()