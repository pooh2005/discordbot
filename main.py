import os
import discord
from discord.ext import commands

from myserver import server_on

# ตั้งค่า intent เพื่อให้บอทเข้าถึงข้อความและข้อมูลของผู้ใช้
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents)

# เก็บคีย์ที่ถูกต้อง (สามารถปรับให้มาจากฐานข้อมูลหรือไฟล์ก็ได้)
valid_keys = ["trc", "tx"]  # คุณสามารถเพิ่มคีย์ที่ถูกต้องได้ที่นี่

# สร้าง dictionary เพื่อเก็บสถานะการใส่คีย์ของผู้ใช้
authorized_users = {}

# กำหนด event เมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# คำสั่งให้ผู้ใช้ใส่คีย์
@bot.command()
async def key(ctx, user_key: str):
    if user_key in valid_keys:
        authorized_users[ctx.author.id] = True
        await ctx.send(f"✅ คีย์ถูกต้อง! คุณสามารถใช้คำสั่ง -script ได้แล้ว")
    else:
        authorized_users[ctx.author.id] = False
        await ctx.send("❌ คีย์ไม่ถูกต้อง! กรุณาลองใหม่")

# คำสั่งเพื่อรับสคริปต์
@bot.command()
async def script(ctx):
    # เช็คว่าผู้ใช้ใส่คีย์ที่ถูกต้องหรือไม่
    if authorized_users.get(ctx.author.id, False):
        script_content = """
      print("Genartion")
        """
        await ctx.author.send(f"นี่คือสคริปต์ของคุณ:\n```python\n{script_content}\n```")
    else:
        await ctx.send("❌ คุณไม่มีสิทธิ์เข้าถึงสคริปต์ กรุณาใส่คีย์ที่ถูกต้องก่อน")

# เพิ่มโค้ดเพื่อรันบอท

server_on()

bot.run(os.getenv('TOKEN'))
