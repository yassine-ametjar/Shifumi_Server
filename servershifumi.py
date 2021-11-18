#!/usr/bin/env python3
# -*- coding: utf-8 -

import asyncio, socket,random

async def send(writer, msg):
    writer.write(msg.encode()+ b"\r\n")

async def receive(reader):
    data =  reader.readline()
    data = data.decode()
    return data
    
async def handle_request(reader,writer):
    msg = "200 : Connexion établie"
    await send(writer,msg)

    mode = await reader.readline()
    mode = mode.decode()
    if (mode == "MODE: 0\r\n"):
        msg = "200 : Choix de Partie"
        await send(writer,msg)
        
        nbround = await reader.readline()
        nbround = nbround.decode()
        nbround = (int)(nbround[10])
        scoreJoueur = 0
        scoreIA = 0
        msg = "200 : Play"
        await send(writer,msg)
        while(nbround > 0):
            msg = str(300 + nbround)+":"+str(scoreJoueur)+"-"+str(scoreIA)
            await send(writer,msg)
            #La partie commence
            choix = await reader.readline()
            choix = choix.decode()
            choixIA = random.randint(0,2)
            if (int(choix[6]) == 1 and choixIA == 0 or \
                int(choix[6]) == 2 and choixIA == 1 or \
                int(choix[6]) == 0 and choixIA == 2 ) :
                scoreJoueur += 1
                msg = str(300 + nbround)+":"+str(scoreJoueur)+"-"+str(scoreIA)
                nbround-=1
            elif (choixIA == 1 and int(choix[6])== 0 or \
                choixIA == 2 and int(choix[6]) == 1 or \
                choixIA == 0 and int(choix[6])== 2 )  :
                scoreIA+=1
                msg = str(300 + nbround)+":"+str(scoreJoueur)+"-"+str(scoreIA)
                nbround-=1
            else:
                msg = str(300 + nbround)+":"+str(scoreJoueur)+"-"+str(scoreIA)
            print("Choix"+choix[6]+"-"+str(choixIA))
            print("résultat"+str(scoreJoueur)+"-"+str(scoreIA))
            await send(writer,msg)


    #writer.close()

async def run_server():
    server = await asyncio.start_server(handle_request,'',999)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())