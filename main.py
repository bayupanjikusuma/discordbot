import discord
from discord.ext import commands
from discord.ext import commands
import os
import aiohttp
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Folder untuk menyimpan gambar
SAVE_FOLDER = "saved_images"

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)





# Membuat folder jika belum ada
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

@bot.command(name='save')
async def save_image(ctx):
    """
    Command untuk menyimpan gambar yang di-attach ke pesan
    Penggunaan: !save (dengan attachment gambar)
    """
    
    # Cek apakah ada attachments di pesan
    if not ctx.message.attachments:
        await ctx.send("❌ Tidak ada gambar yang di-attach! Silakan upload gambar terlebih dahulu.")
        return
    
    saved_count = 0
    
    for attachment in ctx.message.attachments:
        # Cek apakah file adalah gambar
        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            try:
                # Membuat nama file unik dengan timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{attachment.filename}"
                filepath = os.path.join(SAVE_FOLDER, filename)
                
                # Menyimpan gambar menggunakan attachment.save()
                await attachment.save(filepath)
                
                # Info tentang file yang disimpan
                file_info = f"""
                📁 **Gambar berhasil disimpan!**
                📝 Nama file: `{attachment.filename}`
                🔗 URL: {attachment.url}
                💾 Disimpan sebagai: `{filename}`
                📊 Ukuran: {attachment.size} bytes
                """
                
                await ctx.send(file_info)
                saved_count += 1
                
            except Exception as e:
                await ctx.send(f"❌ Error saat menyimpan {attachment.filename}: {str(e)}")
        else:
            await ctx.send(f"⚠️ File `{attachment.filename}` bukan gambar yang didukung!")
    
    if saved_count > 0:
        await ctx.send(f"✅ Total {saved_count} gambar berhasil disimpan!")

@bot.command(name='saveinfo')
async def save_info(ctx):
    """
    Command untuk melihat informasi gambar tanpa menyimpan
    Penggunaan: !saveinfo (dengan attachment gambar)
    """
    
    if not ctx.message.attachments:
        await ctx.send("❌ Tidak ada gambar yang di-attach!")
        return
    
    for attachment in ctx.message.attachments:
        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            info = f"""
            📷 **Informasi Gambar:**
            📝 Nama file: `{attachment.filename}`
            🔗 URL: {attachment.url}
            📊 Ukuran: {attachment.size} bytes
            🆔 ID: {attachment.id}
            """
            await ctx.send(info)

@bot.command(name='listimages')
async def list_saved_images(ctx):
    """
    Command untuk melihat daftar gambar yang tersimpan
    Penggunaan: !listimages
    """
    
    if not os.path.exists(SAVE_FOLDER):
        await ctx.send("📁 Folder penyimpanan belum ada.")
        return
    
    files = os.listdir(SAVE_FOLDER)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
    
    if not image_files:
        await ctx.send("📁 Tidak ada gambar yang tersimpan.")
        return
    
    file_list = "\n".join([f"• {file}" for file in image_files[:10]])  # Maksimal 10 file
    
    response = f"📁 **Gambar yang tersimpan** (Total: {len(image_files)}):\n```\n{file_list}\n```"
    
    if len(image_files) > 10:
        response += f"\n... dan {len(image_files) - 10} file lainnya."
    
    await ctx.send(response)


# Alternatif fungsi save dengan download manual (jika attachment.save() tidak bekerja)
async def save_image_manual(attachment, filepath):
    """
    Fungsi alternatif untuk menyimpan gambar secara manual
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    f.write(await response.read())
                return True
            return False


bot.run("TOKEN_BOT_DISCORD_ANDA")