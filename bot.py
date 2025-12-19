import os
import discord
from discord.ext import commands
import asyncio
import subprocess

from myserver import server_on

import subprocess

subprocess.run(["python", "download_model.py"])

tts_queue = asyncio.Queue()
voice_client = None

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- ตัวละครตัวอย่าง ----------------
ANIME_CHARACTERS = {
    "Rem": "rem",
    "Luffy": "luffy",
    "Nezuko": "nezuko"
}

# ---------------- Select Menu ----------------
class AnimeVoiceSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=name,
                description=f"พากย์เสียงตัวละคร {name}",
                value=value
            )
            for name, value in ANIME_CHARACTERS.items()
        ]

        super().__init__(
            placeholder="🎭 เลือกตัวละครอนิเมะ",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"✅ เลือกตัวละคร: **{self.values[0]}**",
            ephemeral=True
        )

# ---------------- Modal (3 ช่อง) ----------------
class SearchCharacterModal(discord.ui.Modal, title="🔍 ค้นหาตัวละครอนิเมะ"):

    character_name = discord.ui.TextInput(
        label="ชื่อตัวละครอนิเมะ",
        placeholder="เช่น Rem, Luffy, Nezuko",
        required=True,
        max_length=50
    )

    anime_name = discord.ui.TextInput(
        label="ชื่ออนิเมะ",
        placeholder="เช่น Re:Zero, One Piece",
        required=True,
        max_length=50
    )

    tts_text = discord.ui.TextInput(
        label="ข้อความที่จะให้พากย์เสียง",
        placeholder="พิมพ์ข้อความที่อยากให้ตัวละครพูด...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=300
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "🎙️ รับข้อมูลเรียบร้อย\n\n"
            f"🎭 ตัวละคร: **{self.character_name.value}**\n"
            f"📺 อนิเมะ: **{self.anime_name.value}**\n"
            f"🔊 ข้อความ:\n```{self.tts_text.value}```",
            ephemeral=True
        )

        # 🔥 จุดต่อพากย์เสียงจริง
        # - connect voice channel
        # - generate audio
        # - play audio

# ---------------- ปุ่มค้นหา ----------------
class SearchCharacterButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="🔍 ค้นหาตัวละคร",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SearchCharacterModal())

# ---------------- View รวม ----------------
class AnimeVoiceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(AnimeVoiceSelect())
        self.add_item(SearchCharacterButton())

# ---------------- Slash Command ----------------
@bot.tree.command(
    name="tts-anim",
    description="เมนูพากย์เสียงตัวละครอนิเมะ"
)
async def tts_anim(interaction: discord.Interaction):

    # เช็กอยู่ในห้องเสียงเท่านั้น
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "❌ กรุณาเข้าห้องเสียงก่อน",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "🎧 เลือกตัวละครหรือค้นหาตัวละครอนิเมะ",
        view=AnimeVoiceView()
    )
    
    async def tts_worker():
    global voice_client

    while True:
        interaction, text = await tts_queue.get()
        channel = interaction.user.voice.channel

        if not voice_client or not voice_client.is_connected():
            voice_client = await channel.connect()

        output = "temp/tts.wav"

        process = await asyncio.create_subprocess_exec(
            "python",
            "vits/infer.py",
            text,
            output
        )
        await process.communicate()

        voice_client.play(discord.FFmpegPCMAudio(output))

        while voice_client.is_playing():
            await asyncio.sleep(0.5)

        tts_queue.task_done()

await tts_queue.put((interaction, self.tts_text.value))

await interaction.response.send_message(
    "📥 เพิ่มข้อความเข้าคิวพากย์แล้ว",
    ephemeral=True
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.loop.create_task(tts_worker())
    print("✅ Bot ready (Render + VITS Light)")
    
MAX_LEN = 150

if len(self.tts_text.value) > MAX_LEN:
    await interaction.response.send_message(
        "❌ ข้อความยาวเกินไป (150 ตัวอักษร)",
        ephemeral=True
    )
    return

    
    
    

# ---------------- Ready ----------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

server_on()

bot.run(os.getenv('TOKEN'))