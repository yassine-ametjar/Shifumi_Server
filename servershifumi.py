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
        scoreJoueur = 0
        scoreIA = 0
        if (int(nbround[10:])>= 0):
            msg = "200 : Play"
            await send(writer,msg)
            msg = str(300 + int(nbround[10:]))+":"+str(scoreJoueur)+"-"+str(scoreIA)
            await send(writer,msg)
            #La partie commence
            choix = await reader.readline()
            choix = choix.decode()
            choixIA = random.randint(0,2)
            if (choix == 0):
                if(choixIA == 0):
                     print("null")
                elif(choixIA == 1):
                    scoreIA +=1
                else:
                    scoreJoueur +=1
            elif (choix == 1):
                if(choixIA == 0):
                    scoreJoueur +=1
                elif(choixIA == 1):
                    print("null")
                else:
                    scoreIA +=1
            elif (choix == 2):
                if(choixIA == 0):
                    scoreIA +=1
                elif(choixIA == 1):
                    scoreJoueur +=1
                else:
                       print("null")
            msg = str(300 + int(nbround[10:]))+":"+str(scoreJoueur)+"-"+str(scoreIA)
            await send(writer,msg)
        else:
            msg = "400 : Play" 
            await send(writer,msg)
        
        msg = "301:1-0"
        await send(writer,msg)
""" 
    
    msg = "301:1-0"
    await send(writer,msg)

    msg = "300:2-0"
    await send(writer,msg) """

    #writer.close()

async def run_server():
    server = await asyncio.start_server(handle_request,'',999)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())