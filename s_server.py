import socket
import threading
host="127.0.0.1"
port=12345
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
nicknames=[]
def broadcast(messages):
    for client in clients:
        client.send(messages)


def handle(client):
    while True:
        try:
            message= client.recv(1024)
            broadcast(message)
        except:
            index= clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f"{nickname} Left the chat".encode("ascii"))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client,addr=server.accept()
        print(f"Connected with {str(addr)}")
        client.send("Nickname".encode("ascii"))
        nicknmae=client.recv(1024).decode("ascii")
        nicknames.append(nicknmae)
        clients.append(client)
        print(f"Nicknames of the client is {nicknmae}")
        broadcast(f"{nicknmae} joined the chat".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))
        thread= threading.Thread(target=handle,args=(client,))
        thread.start()
print("Server is listening")
recieve()
