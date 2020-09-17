from redbot.core import commands
import discord
import json
import requests
import discord
import matplotlib.pyplot as plt
import numpy as np


class Umfrage(commands.Cog):

    api = "https://api.dawum.de/"
        
    #Funktion wird benötigt, um über die Parliament_ID aus der dawum-JSON die Partei zu ziehen    
    def partei(self,i):
        switcher={
                0:"Sonstige",
                1:"CDU/CSU",
                2:"SPD",
                3:"FDP",
                4:"Grüne",
                5:"Linke",
                6:"Piraten",
                7:"AfD",
                8:"Freie Wähler",
                10:"SSW",
                11:"BP",
                13:"PARTEI",
                14:"BVB/FW",
                15:"Tierschutzpartei",
                16:"BIW",
                101:"CDU",
                102:"CSU",
                }
        return switcher.get(i, "Ungültig")

    #Funktion wird benötigt, um für die jeweilige Partei die Farbe festzulegen    
    def farbe(self, i):
        switcher={
                "CDU/CSU":"#000000",
                "SPD":"#E3000F",
                "FDP":"#ffed00",
                "Grüne":"#64a12d",
                "Linke":"#FF00FF",
                "Piraten":"#ff8800",
                "AfD":"#006699",
                "Freie Wähler":"#ff8800",
                "PARTEI":"#880000",
                "CDU":"#000000",
                "CSU":"#000000",
                }
        return switcher.get(i, "nn")


    #Funktion wird benötigt, um über die Institute_ID aus der dawum-JSON das Institut zu ziehen    
    def Institut(self,i):
        switcher={
                1:"Infratest dimap",
                2:"Forsa",
                3:"Kantar (Emnid)",
                4:"GMS",
                5:"INSA",
                6:"Forschungsgruppe Wahlen",
                7:"Trend Research Hamburg",
                9:"Allensbach",
                11:"GESS Phone & Field",
                12:"uniQma",
                13:"YouGov",
                14:"dimap",
                15:"Mentefactum",
                16:"Civey",
                17:"Ipsos",
                18:"Universität Hamburg",
                20:"IM Field",
                21:"Policy Matters",
                21:"pollytix",
                21:"Conoscope",
                }
        return switcher.get(i, "Ungültig")
    
    #Dient später dazu, mittels Kürzel die richtige Umfrage auszugeben
    def Parliament(self,i):
        switcher={
                "btw":0,
                "bw":1,
                "by":2,
                "be":3,
                "bb":4,
                "hb":5,
                "hh":6,
                "he":7,
                "mv":8,
                "ni":9,
                "nw":10,
                "rp":11,
                "sl":12,
                "sn":13,
                "st":14,
                "sh":15,
                "th":16,
                "eu":17,
                }
        return switcher.get(i, "Ungültig")





    @commands.command()
    @commands.cooldown(1,15, commands.BucketType.guild)
    async def umfrage(self,ctx,land = None):

        """Zeigt die letzte Sonntagsfrage für den Bund, EU oder Bundesland der Wahl an"""
        
        #Lade Daten aus JSON
        json_data = requests.request("GET", self.api).json()
        data = json_data["Surveys"]

        #Wenn die Variable "land" leer ist, so nehme BTW, ansonsten ermittle daraus die Parl_ID
        if land is None:
            pruefparl = int(0)
        else:
            land = land.lower()
            pruefparl = self.Parliament(land)

        #Wenn ungültiges Kürzel -> Abbruch
        if pruefparl == "Ungültig":
            return

        pruefparl = int(pruefparl)
        
        #Iteration durch die Umfragen

        for i in data.values(): 
            currparl=int(i["Parliament_ID"]) #Speichere aktuelle Parl_ID


            #Wenn die aktuelle Parl_ID mit der übergebenen überseinstimmt, dann lets go
            
            if pruefparl == currparl:
                
                #Paar Variablen und Listen
                counter = 1
                stopper = len(i["Results"])
                stopper += 1
                day = i["Date"]
                dawum = "https://dawum.de"
                lizenz = "https://opendatacommons.org/licenses/odbl/1.0"
                fig, ax = plt.subplots()
                voter = []
                parties = []
                color = []
                
                #Festlegung der Befragten und des Institus
                institutn = self.Institut(int(i["Institute_ID"]))
                befragte = i["Surveyed_Persons"]
                

                # if-Abfrage wird nur für den Titel im Discord-Embed gebraucht
                if pruefparl == 0:
                    embed = discord.Embed(title="Letzte Sonntagsfrage zur BTW", description=f"Datum: {day}\nBefragte: {befragte}\nInstitut: {institutn}\nDaten von [Dawum]({dawum}) (Lizenz: [ODC-ODbL]({lizenz}))")
                else: 
                    land = land.upper()
                    embed = discord.Embed(title=f"Letzte Sonntagsfrage in {land}", description=f"Datum: {day}\nBefragte: {befragte}\nInstitut: {institutn}\nDaten von [Dawum]({dawum}) (Lizenz: [ODC-ODbL]({lizenz}))")

                #Iteriere über die Survey
                for value in i["Results"]:
                    
                    parteiausgabe = self.partei(int(value))
                    ergebnis = i["Results"][str(value)]
                    nachricht = str(parteiausgabe) + ": " + str(ergebnis)
                    
                    #Wenn die aktuelle "Partei" "Sonstige" ist, so skippe erstmal
                    if int(value) == 0:
                        counter += 1
                        wert = None
                        pass
                    else:
                        wert = float(ergebnis) 
                        ergebnis = str(ergebnis)+"%"
                        embed.add_field(name=parteiausgabe, value=ergebnis, inline=False) #embed-Field hinzufügen
                        counter += 1
                        
                        #Wenn die Variable "wert" leer ist, so skippe, sonst füge die Partei in "parties" und den Umfragewert in "voter" hinzu
                        if wert is None:
                            break
                        else:
                            parties.append(parteiausgabe)
                            voter.append(wert)
                    
                    if counter == stopper:
                        break
                    
                #Umfrageergebnis für Sonstige. Dunno warum ich das yeet genannt habe.    
                yeet = i["Results"][str(0)]    
                wert2 = float(yeet)
                yeet = str(yeet) + "%"
                
                #Folgenden drei Zeilen dienen dazu, auch die Sonstigen in den embed sowie die Listen für die Grafik hinzuzufügen
                embed.add_field(name="Sonstige", value=yeet)
                voter.append(wert2)
                parties.append("Sonstige")

                y_pos = np.arange(len(voter)) #Keine Ahnung was es macht, wird aber für die Grafik benötigt, die sonst scheiße aussieht
                

                #Bindung der Farben an die Parteien
                for i in parties:
                    farbe = self.farbe(i)
                    if farbe == "nn":
                        color.append("#c0c0c0")
                    else:
                        color.append(self.farbe(i))
               
                #Grafiksachen
                ax.set_xticks(range(len(parties))) #Abstände auf x-Achse
                ax.set_xticklabels(parties, rotation='vertical') #Werte auf x-Achse
                plt.axhline(y=5,ls='--',linewidth=0.5,color='#000000') #5%-Linie
                ax.spines['top'].set_visible(False) #Topline entfernt
                ax.spines['right'].set_visible(False) #Rightline entfernt
                ax.set_facecolor('#e7eef4') #Hintergrundfarbe
                plt.tight_layout() #Anpassung der Grafik an den Plot

                plt.bar(y_pos, voter, align="center",color=color) #Erstellen des Plots
                plt.savefig('/home/strator/Umfrage.png', dpi=300, facecolor='#e7eef4') #Speichere die Grafik. Speicherpfad kann geändert werden, dann aber bitte darauf achten, dass dies auch unten beim Senden gemacht wird. 
                break

        await ctx.send(embed=embed) #Sende embed
        await ctx.send(file=discord.File('/home/strator/Umfrage.png', 'Umfrage.png')) #Sende Grafik

        voter.clear() #Lustigerweise bleibt die Liste nach dem Ausführen des Codes. Daher muss hier einmal geleert werden

    #Wenn Cooldown dann lösche Nachricht
    @umfrage.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
