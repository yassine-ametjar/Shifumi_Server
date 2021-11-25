#!/usr/bin/env python3
# -*- coding: utf-8 -

import asyncio,random
from datetime import datetime

tablenameless = {}
tablename= {}

def log_envoyer(chevron,msg,writer):
    f = open("shared/shifumi.log", "a")
    ip = writer.get_extra_info('peername')[0]
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S\n")
    f.write(chevron+" "+ip+" "+msg+" "+date)
    f.close()

async def send(writer, msg):
    writer.write(msg.encode()+ b"\r\n")
    log_envoyer(">>>",msg,writer)

async def receive(reader,writer):
    msg = await reader.readline()
    msg = msg.decode()
    log_envoyer("<<<",msg.strip(),writer)
    return msg

async def IA(writer,reader):
    msg = "200: Choix de Partie"
    await send(writer,msg)

    nbrounds = await receive(reader,writer)
    nbrounds = nbrounds.strip()
    nbrounds = (int)(nbrounds[10:])

    scoreJoueur = 0
    scoreIA = 0
    while(True):
        if(nbrounds > 0 ):
            msg = "200: Play"
            break
        else:
            msg = "400: Faut écrire un chiffre strictement positif"
            await send(writer,msg)
            nbrounds = await receive(reader,writer)
            nbrounds = (int)(nbrounds[10:])
    await send(writer,msg)  
    msg = str(300 + nbrounds)
    await send(writer,msg)
    while(nbrounds > 0):
        #La partie commence
        choix = await receive(reader,writer)
        choix = choix.strip()
        choix = int(choix[6:])
        choixIA = random.randint(0,2)
        if (choix == 1 and choixIA == 0 or \
            choix == 2 and choixIA == 1 or \
            choix == 0 and choixIA == 2 ) :
            scoreJoueur += 1
            if (nbrounds-1 == 0):
                if (scoreJoueur > scoreIA):
                    msge = "300: Vous avez gagné "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
                elif (scoreJoueur < scoreIA):
                    msge = "300: Vous avez perdu "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
                else :
                    msge = "300: Match Nul "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
            nbrounds-=1
            msg = str(300 + nbrounds)+":"+" Coups : ( Joueur : "+str(choix)+" IA : "+str(choixIA)+") Score : ( Joueur : "+str(scoreJoueur)+" IA : "+str(scoreIA)+" )"
        elif (choixIA == choix):
            msg = str(300 + nbrounds)+":"+" Coups : ( Joueur : "+str(choix)+" IA : "+str(choixIA)+") Score : ( Joueur : "+str(scoreJoueur)+" IA : "+str(scoreIA)+" )"
        else:
            scoreIA += 1
            if (nbrounds-1 == 0):
                if (scoreJoueur > scoreIA):
                    msge = "300:Vous avez gagné "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
                elif (scoreJoueur < scoreIA):
                    msge = "300:Vous avez perdu "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
                else :
                    msge = "300:Match Nul "+str(scoreJoueur)+"-"+str(scoreIA)
                    await send(writer,msge)
            nbrounds-=1
            msg = str(300 + nbrounds)+":"+" Coups : ( Joueur : "+str(choix)+" IA : "+str(choixIA)+") Score : ( Joueur : "+str(scoreJoueur)+" IA : "+str(scoreIA)+" )"
        await send(writer,msg)

async def partie(reader1,writer1,reader2,writer2,nbrounds):
    scoreJoueur1 = 0
    scoreJoueur2 = 0
    msg = str(300 + nbrounds)
    await send(writer2,msg)
    await send(writer1,msg)
    while (nbrounds>0):
        choix1 = await receive(reader1,writer1)
        choix1 = int(choix1[6])
        choix2 = await receive(reader2,writer2)
        choix2 = int(choix2[6])
        if  (choix1 == 1 and choix2 == 0 or \
            choix1 == 2 and choix2 == 1 or \
            choix1 == 0 and choix2 == 2 ):
            scoreJoueur1 += 1
            if (nbrounds-1 == 0):
                if (scoreJoueur1 > scoreJoueur2):
                    msge = "300:Vous avez gagné "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    msgee = "300:Vous avez perdu "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msge)
                    await send(writer2,msgee)
                    
                elif (scoreJoueur1 < scoreJoueur2):
                    msge = "300:Vous avez gagné "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    msgee = "300:Vous avez perdu "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msgee)
                    await send(writer2,msge)
                else :
                    msge = "300: Match Nul "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msge)
                    await send(writer2,msge)
            nbrounds-=1
            msg = str(300 + nbrounds)+":"+"Coups : ( Joueur1 : "+str(choix1)+" Joueur2 : "+str(choix2)+") Score : ( Joueur1 : "+str(scoreJoueur1)+" Joueur2 : "+str(scoreJoueur2)+" )"
        elif (choix2 == choix1):
            msg = str(300 + nbrounds)+":"+"Coups : ( Joueur1 : "+str(choix1)+" Joueur2 : "+str(choix2)+") Score : ( Joueur1 : "+str(scoreJoueur1)+" Joueur2 : "+str(scoreJoueur2)+" )"
        else:
            scoreJoueur2 += 1
            if (nbrounds-1 == 0):
                if (scoreJoueur1 > scoreJoueur2):
                    msge = "300:Vous avez gagné "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    msgee = "300:Vous avez perdu "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msge)
                    await send(writer2,msgee)
                elif (scoreJoueur1 < scoreJoueur2):
                    msge = "300:Vous avez gagné "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    msgee = "300:Vous avez perdu "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msgee)
                    await send(writer2,msge)
                else :
                    msge = "300:Match Nul "+str(scoreJoueur1)+"-"+str(scoreJoueur2)
                    await send(writer1,msge)
                    await send(writer2,msge)
            nbrounds-=1
            msg = str(300 + nbrounds)+":"+"Coups : ( Joueur1 : "+str(choix1)+" Joueur2 : "+str(choix2)+") Score : ( Joueur1 : "+str(scoreJoueur1)+" Joueur2 : "+str(scoreJoueur2)+" )"
        await send(writer1,msg)
        await send(writer2,msg)
    tablenameless.clear()

async def nameless(writer,reader):
    msg = "200: Choix de Partie"
    await send(writer,msg)
    nbrounds = await receive(reader,writer)
    nbrounds = (int)(nbrounds[10:])
    msg = ""
    while(msg != "200: Play"):
        if(nbrounds > 0 ):
            msg = "200: Play"
        else:
            msg = "400: Faut écrire un chiffre strictement positif"
            await send(writer,msg)
            nbrounds = await receive(reader,writer)
            nbrounds = (int)(nbrounds[10:])
    await send(writer,msg)
    #lorsque y'a déjà le nb round dans la tablenameless
    if  nbrounds in tablenameless :
        msg = "201: Starting game Now"
        await send(writer,msg)
        if (len(tablenameless[nbrounds]) > 0):
            writer1 = tablenameless[nbrounds].pop()
            reader1 = tablenameless[nbrounds].pop()
            del tablenameless[nbrounds]
            await partie(reader1,writer1,reader,writer,nbrounds)
    # on le renvoie en attente
    else :
        msg = "202: Waiting for an oponent"
        await send(writer,msg)
        tablenameless[nbrounds] = [reader,writer]

async def createtable(writer,reader):
    msg = "200:Choix de Partie"
    await send(writer,msg)
    while (True):
        tname = await receive(reader,writer)
        l = len(tname)-2
        tname = tname[7:l]
        tname = tname.strip()
        if(tname in tablename or len(tname) == 0):
            msg = "400:Saisissez un nom de table valide"
            await send(writer,msg)
        else:
            msg = "200:Commencer"
            await send(writer,msg)
            nbrounds = await receive(reader,writer)
            nbrounds = (int)(nbrounds[10:])
            msg = ""
            while(msg != "202: Waiting for an oponent"):
                if(nbrounds > 0 ):
                    msg = "202: Waiting for an oponent"
                else:
                    msg = "400:Faut écrire un chiffre strictement positif"
                    await send(writer,msg)
                    nbrounds = await receive(reader,writer)
                    nbrounds = (int)(nbrounds[10:])
            await send(writer,msg)
            tablename[tname] = [reader,writer,nbrounds]
            break

async def joinname(writer,reader):
    msg = "200: Choix de Partie"
    await send(writer,msg)
    tname = await receive(reader,writer)
    l = len(tname)-2
    tname = tname[7:l]  
    tname = tname.strip() 
    if (len(tname) == 0) :
        msg = "500:Vous n'avez rien écrit"
        await send(writer,msg)  
    elif (tname  not in tablename):
        msg = "500:Saisissez un nom de table valide"
        await send(writer,msg)
    else:
        msg = "201: Starting game Now"
        await send(writer,msg)
        if (len(tablename[tname]) > 0):
            nbrounds = tablename[tname].pop()
            writer1 = tablename[tname].pop()
            reader1 = tablename[tname].pop()
            del tablename[tname]
            await partie(reader1,writer1,reader,writer,nbrounds)

async def handle_request(reader,writer):
    msg = "200 : Connexion établie"
    await send(writer,msg)  
    
    mode = await receive(reader,writer)

    if (mode == "MODE: 0\r\n"):
        await IA(writer,reader)
    elif (mode == "MODE: 1\r\n"):
        await nameless(writer,reader)
    elif (mode == "MODE: 2\r\n"):
        await createtable(writer,reader)
    elif (mode == "MODE: 3\r\n"):
        await joinname(writer,reader)

async def run_server():
    server = await asyncio.start_server(handle_request,'',999)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())