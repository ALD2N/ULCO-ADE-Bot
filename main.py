import requests
from icalendar import Calendar, Event
import datetime
import pytz
import time
import discord
import asyncio
import tokenBot
from discord.ext import tasks
import pickle

client = discord.Client()
@client.event
async def on_ready():
    print("I'm ready.")

@tasks.loop(seconds=10)
async def loop():
    print("start loop")
    # url = 'http://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021420e3a5ae4684db56b885e8a1d1455f2f8a4b5d21e20190d5fa8140985607ae3d30b5444b6147df22fbd9046fec7a51a559ca4c0e828e7c479f1e952f6d94a89994e44634fdadfcaf68223caeaaf4f3216bfdc022fb73c01a5ac9fc83b122c1dcf9c4bc151f5a34002a955799f64eee2ef377b612dec2c5fba5147d40716acb1388637ba1215f9317'
    # r = requests.get(url, allow_redirects=True,verify=False)
    # open('calendar.ics', 'wb').write(r.content)
    g = open('calendar.ics','rb')
    gcal = Calendar.from_ical(g.read())
    g.close()
    a_file = open("listeCours.pkl", "rb")
    listeCoursBase = pickle.load(a_file)
    a_file.close()
    listeCours = {}
    for component in gcal.walk():
        if component.name == "VEVENT":

            nomCours = str(component.get('summary'))
            # on passe les heures au format GMT+1 français 
            dtstart = component.get('dtstart').dt.astimezone(pytz.timezone('Europe/Paris'))
            dtend = component.get('dtend').dt.astimezone(pytz.timezone('Europe/Paris'))
            UID = component.get('UID')
            listeCours[UID] = [nomCours, dtstart, dtend]
    if listeCoursBase == {}:
        listeCoursBase = listeCours
        await channel.send("Initialisation base de donnée terminée")
        a_file = open("listeCours.pkl", "wb")
        pickle.dump(listeCours, a_file)
        a_file.close()

    else:
        if(listeCoursBase != listeCours):
            # on donne l'élément différent entre les deux listes
            if(len(listeCours) > len(listeCoursBase)):
                for key in listeCours:
                    if key not in listeCoursBase:
                        if datetime.date.today().month == listeCours[key][1].month and (listeCours[key][1].day-datetime.date.today().day) <= 4 :
                            embed=discord.Embed(title="COURS AJOUTÉ", description="un cours sauvage surgit des hautes herbes", color=0x00ccff)
                            embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/flat-design-database-set-1/24/button-filledcircle-add-512.png")
                            embed.add_field(name=listeCours[key][0], value="le "+ str(listeCours[key][1].day) +"/"+ str(listeCours[key][1].month) +"/"+ str(listeCours[key][1].year)+" de " + str(listeCours[key][1].time()) + " a " + str(listeCours[key][2].time()), inline=True)
                            embed.add_field(name="Les personnes concernés sont :", value="<@&892730784958533712>", inline=True)
                            await channel.send(embed=embed)
            else:
                for key in listeCoursBase:
                    if key not in listeCours:
                        if datetime.date.today().month == listeCoursBase[key][1].month and (listeCoursBase[key][1].day-datetime.date.today().day) <= 4 :
                            embed=discord.Embed(title="COURS SUPPRIMÉ", description="un cours s'est enfuis", color=0x00ccff)
                            embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/basic-ui-elements-coloricon/21/19-512.png")
                            embed.add_field(name=listeCoursBase[key][0], value="le "+ str(listeCoursBase[key][1].day) +"/"+ str(listeCoursBase[key][1].month) +"/"+ str(listeCoursBase[key][1].year)+" de " + str(listeCoursBase[key][1].time()) + " a " + str(listeCoursBase[key][2].time()), inline=True)
                            embed.add_field(name="Les personnes concernés sont :", value="<@&892730784958533712>", inline=True)
                            await channel.send(embed=embed)
            listeCoursBase = listeCours
            a_file = open("listeCours.pkl", "wb")
            pickle.dump(listeCours, a_file)
            a_file.close()


@client.event
async def on_message(message):
    if message.content == "!init" and not 'channel' in locals():
        print("Initialisation en cours")
        global channel
        idx = 0
        channel = message.channel
        global listeCoursBase
        listeCoursBase = {}

        a_file = open("listeCours.pkl", "wb")
        pickle.dump(listeCoursBase, a_file)
        a_file.close()

        print("Initialisation du salon terminée")
        print("<@&892730784958533712>")
        await channel.send("Mise en ligne, récupération de l'edt toute les 30 minutes lancée")
        loop.start()





client.run(tokenBot.get_token())