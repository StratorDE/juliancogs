from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
from redbot.core import i18n 
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.bot import Red
import discord
import random
import asyncio
from dpymenus import Page, PaginatedMenu


_ = i18n.Translator("Core", __file__)

class Teststore(commands.Cog):
	def __init__(self, bot: "Red"):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=991991)
		self.config.register_user(
				comments={}
		)

	#Kommentare hinzufügen
	@commands.command()
	async def addentry(self, ctx, Benutzer: discord.User,*text):
		zaehler = 0
		while zaehler < 99:

			try:
				await self.config.user(Benutzer).comments.get_raw(zaehler)
				zaehler +=1
			except KeyError:
				await self.config.user(Benutzer).comments.set_raw(
					zaehler, value={'text': text}
					)
				zaehler = 100
				await ctx.message.add_reaction('✅')
				return

	#Kommentare entfernen
	@commands.command()
	@checks.is_owner()
	async def delentry(self, ctx,Benutzer: discord.User, index):
		#index = str(index)
		#INdex als Beispiel 3
		try:
			nachricht = " ".join(await self.config.user(Benutzer).comments.get_raw(str(index), 'text'))
			await self.config.user(Benutzer).comments.clear_raw(index)
			zaehler = int(index)
			
			while zaehler < 100:
				zaehler +=1 #Zaehler auf 4
				try:
					msgup = await self.config.user(Benutzer).comments.get_raw(str(zaehler), 'text') #Hole Daten von Platz 4 
					zaehler2 = zaehler - 1 #Wir brauchen eine Variable, die jetzt eins niedriger als zaehler ist, zaehler2 ist 3
					await self.config.user(Benutzer).comments.set_raw( #das von Platz 4 wird auf Platz 3 gesetzt
							zaehler2, value={'text': msgup}
							)
					await self.config.user(Benutzer).comments.clear_raw(str(zaehler))
				except KeyError: 
					break
				
			await ctx.send(f"Nachricht '{nachricht}' von {Benutzer} gelöscht")
			
		except KeyError:
			await ctx.send("Ich konnte keine Nachricht dazu finden..")

	#Kommentare anzeigen
	@commands.command()
	async def listcomments(self, ctx, Benutzer: discord.User):
		zaehler = 0
		embed = discord.Embed()
		embed.title = f"Nachrichten von {Benutzer}"
		embed.set_thumbnail(url=Benutzer.avatar_url_as(static_format='png'))

		while zaehler < 25:
			try:
				insert = ' '.join(await self.config.user(Benutzer).comments.get_raw(str(zaehler), 'text'))
				embed.add_field(name=f"{zaehler}",value=f" {insert}",inline=False)
				zaehler +=1
			except KeyError:
				zaehler +=1

		await ctx.send(embed=embed)

		embed2 = discord.Embed()
		embed2.title = f"Nachrichten von {Benutzer}"
		embed2.set_thumbnail(url=Benutzer.avatar_url_as(static_format='png'))
		while zaehler < 50:
			try:
				insert = ' '.join(await self.config.user(Benutzer).comments.get_raw(str(zaehler), 'text'))
				embed2.add_field(name=f"{zaehler}",value=f" {insert}",inline=False)
				zaehler +=1
			except KeyError:
				zaehler +=1
				break

		await ctx.send(embed=embed2)

		embed3 = discord.Embed()
		embed3.title = f"Nachrichten von {Benutzer}"
		embed3.set_thumbnail(url=Benutzer.avatar_url_as(static_format='png'))
		while zaehler < 75:
			try:
				insert = ' '.join(await self.config.user(Benutzer).comments.get_raw(str(zaehler), 'text'))
				embed3.add_field(name=f"{zaehler}",value=f" {insert}",inline=False)
				zaehler +=1
			except KeyError:
				zaehler +=1
				break

		try:
			insert = ' '.join(await self.config.user(Benutzer).comments.get_raw(str(25), 'text'))
		except KeyError:
			return
		await ctx.send(embed=embed3)
	
	#Ausgabe eines Menues fuer die gespeicherten Nachrichten eines Nutzers
	@commands.command()
	async def msgmenu(self, ctx, Benutzer: discord.User):
		zaehler = 0
		zaehler2 = 0
		zaehler3 = 0
		pagelist = []
		pagelist.append(Page(title='Seite 1'))
		nachrichtlist = []
		while True:
			try:
				#Discord-Embeds koennen nur 24 Eintraege pro Seite. Sobald hier die 25 erreicht wird, wird ein neues Objekt in der Liste gespeichert und der zaehler resettet
				if zaehler == 25:
					zaehler2 +=2
					pagelist.append(Page(title=f'Seite {zaehler2}'))
					zaehler2 -=1
					zaehler = 0
				insert = ' '.join(await self.config.user(Benutzer).comments.get_raw(str(zaehler3), 'text')) #Ich hole mir hier die Nachricht des Benutzers nach dem Wert von zaehler3
				pagelist[zaehler2].add_field(name=f"{zaehler3}",value=f" {insert}",inline=False) #Neues Embed-Field wird angelegt, mit dem Wert von zaehler3 als Name und dem Wert von insert als Value 
				zaehler +=1
				zaehler3 +=1
			except KeyError:
				break



		#Alter Code hier unten. Habe das vereinfacht und speichere die Nachricht nicht mehr in einer eigenen Liste -> Spart etwas an Leistung

		#zaehler = 0
		#zaehler2 = 0
		#zaehler3 = 0
		#for i in nachrichtlist:
	#		if zaehler == 25:
#				zaehler2 +=2
#				testlist.append(Page(title=f'Seite {zaehler2}'))
#				zaehler2 -=1
#				zaehler = 0
#			testlist[zaehler2].add_field(name=f"{zaehler3}",value=f" {i}",inline=False)
		#	zaehler +=1
	#		zaehler3 +=1
		menu = PaginatedMenu(ctx)
		menu.set_timeout(25)
		menu.add_pages(pagelist)
		await menu.open()




	#Zufaelligen Kommentar eines Users ausgeben
	@commands.command()
	async def quote(self,ctx,Benutzer: discord.User):
		zaehler = 0

		while zaehler < 101:
			try:
				await self.config.user(Benutzer).comments.get_raw(str(zaehler),'text')
				zaehler +=1


			except KeyError:
				break

		zaehler -=1
		randint=random.randint(0,zaehler)
		nachricht = " ".join(await self.config.user(Benutzer).comments.get_raw(str(randint), 'text'))
		await ctx.send(nachricht)


	#Purge Kommentare eines Nutzer. Mit Vorsicht zu genießen!		
	@commands.command()
	@checks.is_owner()
	async def purgecomments(self, ctx: commands.Context,Benutzer: discord.User):
		bot = self.bot    
		await ctx.send(_("Bist du sicher? (y/n)"))

		pred = MessagePredicate.yes_or_no(ctx)
		try:
			await self.bot.wait_for("message", check=pred)
		except asyncio.TimeoutError:
			await ctx.send(_("Response timed out."))
			return
		else:
			if pred.result is True:
				zaehler = 0

				while zaehler < 101:
					try:
						await self.config.user(Benutzer).comments.clear_raw(str(zaehler))
						zaehler +=1
					except KeyError:
						zaehler = 101
						break

			await ctx.send('✅')
