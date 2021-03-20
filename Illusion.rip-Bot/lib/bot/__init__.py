from datetime import datetime
from glob import glob

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound


PREFIX = "*"
OWNER_IDS = [422756717277872138]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"Cog: {cog} successfully loaded")

		print("Setup completed")

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

			print("IlllusionBot is now running...")
			super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("IlllusionBot connected.")

	async def on_disconnect(self):
		print("IlllusionBot è disconnected.")

	async def on_error(self, err, **args, **kwags):
		if err == "on_command_error":
			await args[0].send("Someting went wrong.")

		raise

	async def on_command_error(self, ctx, exc, ext):
		if isinstance(ext, CommandNotFound):
			await ctx.send("Comando inesistente. Controlla l'ortografia")

		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(816991544015847436)
			print("IlllusionBot ready.")

		else:
			print("IlllusionBot reconnected.")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)



bot = Bot()