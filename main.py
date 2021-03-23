import discord
import os
import datetime
from datetime import timedelta
from time import sleep
from keepAlive import keep_alive

client = discord.Client()

customEmoji1 = "eis"
positive = "👍"
negative = "👎"
maybe = "🤷"

raidCombList = ["Dienstag;20:00;2",
                "Mittwoch;20:00;3",
                "Donnerstag;20:00;4",
                "Freitag;20:00;5",
                "Samstag;15:00;6",
                "Samstag;20:00;6",
                "Sonntag;15:00;0",
                "Sonntag;20:00;0",
                "Montag;20:00;1"
                ]  # liste von Raidterminen: [Wochentag;Uhrzeit;Wochentag als Zahl(Sonntag = 0, Samstag = 6)]

pEmoji1 = "🟦"
pEmoji2 = "🟩"
pEmoji3 = "🟨"
pEmoji4 = "🟥"
pEmojiX = "✅"

pExplain = "**Erklärung für Prioritäts-Abstimmung:**\n\
            `" + pEmoji1 + "` Ich möchte, weil ich noch was brauch\n\
            `" + pEmoji2 + "` Ich möchte, weil ich bock hab, lasse aber anderen, die noch was brauchen, den Vortritt\n\
            `" + pEmoji3 + "` Ich mach mit wenn jemand fehlt\n\
            `" + pEmoji4 + "` Ich möchte auf gar keinen fall\n\
            `" + pEmojiX + "` mir is alles egal ich will einfach irgendwas raiden"

pRaidList = ["Deep Stone Crypt"
             "Garden of Salvation"
             "Last Wish"
             "Last Wish - only Riven(3x)"
             "Ich möchte einfach raiden - egal was"
             ]
pX = "mir is alles egal ich will einfach irgendwas raiden"

wishEffects = [
    "grants an Ethereal Key.",
    "spawns the ship-chest between Morgeth and the Vault(Glittering Key needed).",
    "unlocks an Emblem.",
    "teleports the fireteam to Shuro Chi.",
    "teleports the fireteam to Morgeth.",
    "teleports the fireteam to the Vault.",
    "teleports the fireteam to Riven.",
    "will play the song, Hope for the Future.",
    "Failsafe comments the Raid.",
    "The Drifter comments the Raid.",
    "activates Confetti mode",
    "fancy Hats",
    "activates Petra's Run.",
    "spawns Corruptes eggs."

]
helopText = "Available Commands: \n\
      `!throne`: Shattered Throne 1st Encounter map \n\
      `!heresy`: Pit of Heresy 4th Encounter map \n\
      `!dsc 1`: DSC 1st Encounter map \n\
      `!dsc 3`: DSC 3rd Encounter map\n\
      `!wish all`: Overview over all Wishes \n\
      `!wish` + number(1-14): shows the selected wish\n\
      `!wahrheit`: Beschert dir die Erleuchtung nach der du dein Leben lang gesucht hast! "

"""def log(text):
    with open("log.csv", "a") as file:
        file.write(text + "\n")"""


@client.event
async def on_ready():
    nowDay = (datetime.datetime.now()).strftime("%d")
    nowMonth = (datetime.datetime.now()).strftime("%m")
    nowYear = (datetime.datetime.now()).strftime("%Y")
    nowTime = (datetime.datetime.now()).strftime("%X")
    now = nowDay + "." + nowMonth + "." + nowYear + " " + nowTime

    print('{0.user} is online at '.format(client) + now)


@client.event
async def on_message(message):
    # function Setup
    def loggeneral():
        with open("log.csv", "a") as file:
            file.write(message.author.name + ";" + now + ";" + message.content + "\n")

    async def wp():
        await message.delete()

        addent = int((datetime.datetime.now()).strftime("%w"))
        addent += -2
        if addent >= 3:
            addent += -7

        date = datetime.datetime.now() - timedelta(days=addent)

        for raidComb in raidCombList:
            raidComb = raidComb.split(";")
            raidDay = raidComb[0]
            raidTime = raidComb[1]

            if date.strftime("%w") != raidComb[2]:
                # verhindert das bei wiederholung von wochentagen das datum erhöht wird
                date = date + timedelta(days=1)

            rDay = date.strftime("%d")
            month = date.strftime("%m")
            # year = date.strftime("%Y")
            dateToPrint = rDay + "." + month + "."  # + year
            await message.channel.send(raidDay + " " + dateToPrint + " " + raidTime)

    async def wpraids():
        await message.delete()
        await message.channel.send(pExplain)
        for raid in pRaidList:
            await message.channel.send(raid)


    # time Setup
    nowDay = (datetime.datetime.now()).strftime("%d")
    nowMonth = (datetime.datetime.now()).strftime("%m")
    nowYear = (datetime.datetime.now()).strftime("%Y")
    nowTime = (datetime.datetime.now()).strftime("%X")
    now = nowDay + "." + nowMonth + "." + nowYear + " " + nowTime

    # Reactions
    # Reactions RaidDates
    if message.author == client.user:
        for day in raidCombList:

            if (message.content.split(" "))[0] == day.split(";")[0]:
                # await message.add_reaction(discord.utils.get(client.emojis, name=customEmoji1))
                await message.add_reaction(positive)
                await message.add_reaction(negative)
                await message.add_reaction(maybe)

    # Reactions RaidPriority
    if message.author == client.user:
        for raidName in pRaidList:

            if message.content == raidName:
                await message.add_reaction(pEmoji1)
                await message.add_reaction(pEmoji2)
                await message.add_reaction(pEmoji3)
                await message.add_reaction(pEmoji4)

        if message.content == pX:
            await message.add_reaction(pEmojiX)

    # ignoring bots
    if message.author == client.user:
        return

    # commands
    if "!throne" in message.content:
        loggeneral()
        await message.delete()
        await message.channel.send("Shattered Throne: 1st Encounter map:")
        await message.channel.send(file=discord.File("guides/throne.png"))

    if "!heresy" in message.content or "!pit" in message.content:
        loggeneral()
        await message.delete()
        await message.channel.send("Pit of Heresy: 4th Encounter map:")
        await message.channel.send(file=discord.File("guides/heresy.png"))

    if "!wish" in message.content:
        loggeneral()
        await message.delete()
        number = message.content.split("!wish ")[1]
        if number == "all":
            i = 0
            for effect in wishEffects:
                i = i + 1
                await message.channel.send(str(i) + ". Wish: " + effect)
        else:
            await message.channel.send(number + ". Wish: " + wishEffects[int(number) - 1])
            await message.channel.send(file=discord.File("guides/wishes/wish-" + number + ".jpg"))

    if "!dsc" in message.content:
        loggeneral()
        await message.delete()
        number = message.content.split("!dsc ")[1]
        if number == 1 or 3:
            await message.channel.send("DSC " + number + ". Encounter map: ")
            await message.channel.send(file=discord.File("guides/DSC/crypta_map_0" + number + ".png"))

    if "!helöp" in message.content:
        loggeneral()
        await message.delete()
        await message.channel.send(helopText)

    if "!wahrheit" in message.content:
        loggeneral()
        await message.channel.send("Robin hat Recht!")

    if "!xxtime" in message.content:
        loggeneral()
        await message.delete()
        xxtime = (datetime.datetime.now()).strftime("%c")
        for i in range(1, 60):
            if xxtime != (datetime.datetime.now()).strftime("%c"):
                xxtime = (datetime.datetime.now()).strftime("%c")
                await message.channel.send(xxtime)
            else:
                sleep(0.49)

    if "!wp" in message.content:
        loggeneral()
        await wp()

    if "!wpx" in message.content:
        loggeneral()
        await wp()
        await wpraids()

    if "!send" in message.content:
        text = message.content
        text = text.replace("!send", "")

        loggeneral()
        await message.channel.send(text)
        await message.delete()

    if "!nein" in message.content:
        await message.delete()
        loggeneral()
        for i in range(5):
            await message.channel.send("**NEIN**")

    if "!clear" in message.content:
        loggeneral()
        args = message.content.split(" ")
        if len(args) == 2 and args[1].isdigit():
            limit = int(args[1]) + 1
            deleted = await message.channel.purge(limit=limit)
            await message.channel.send("{} messages deleted.".format(len(deleted) - 1))
            sleep(0.7)
            await message.channel.purge(limit=1)
        elif args[1] == "x":
            await message.channel.send("You got me there xD")
        else:
            await message.channel.send("`!clear x` clears x messages. \n Your command doesn't fit this pattern!")


keep_alive()
client.run(os.getenv('TOKEN'))
