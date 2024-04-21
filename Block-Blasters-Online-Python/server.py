#SERVER


import socket
from _thread import *
import threading
import pygame
import pickle
server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()



players = [None, pygame.Rect(2, 2, 18, 18), pygame.Rect(462, 462, 18, 18)]
pos = [None, 2, 462]
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    conn.send(bytes(f'{str(pos[player])}', 'utf-8'))
    players[0] = None
    players[1] = bytes('(2, 2, -100, -100, 2)', 'utf-8')
    players[2] = bytes('(462, 462, -100, -100, 2)', 'utf-8')
    reply = ""
    while True:
        try:
           
            data = conn.recv(2048*5)
            
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 2:
                    reply = players[1]
                else:
                    reply = players[2]
                
            
            if event.is_set() == False:
                
                reply = b'wait'
            x1 = players[1].decode('utf-8').strip(')(').split(', ') [0]
            y1 = players[1].decode('utf-8').strip(')(').split(', ') [1]
            bx1 = players[1].decode('utf-8').strip(')(').split(', ') [2]
            by1 = players[1].decode('utf-8').strip(')(').split(', ') [3]
            x2 = players[2].decode('utf-8').strip(')(').split(', ') [0]
            y2 = players[2].decode('utf-8').strip(')(').split(', ') [1]
            bx2 = players[2].decode('utf-8').strip(')(').split(', ') [2]
            by2 = players[2].decode('utf-8').strip(')(').split(', ') [3]

            if x1 == bx2 and y1 == by2:
                if player == 2:
                    reply = b'win'
                else:
                    reply = b'lose'
            if x2 == bx1 and y2 == by1:
                if player == 2:
                    reply = b'lose'
                else:
                    reply = b'win'

            
            
            conn.sendall(reply)
        except:
            break

    print("Lost connection")
    conn.close()
event = threading.Event()
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    currentPlayer += 1
    if currentPlayer == 2:
        print('client 2 accpeted')
        event.set()
        print('event set and 2nd client about to be created')
    start_new_thread(threaded_client, (conn, currentPlayer))


