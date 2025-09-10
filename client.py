##########################################################################
#                                                                        #
# Name: Mhlengeni Miya                                                   #
#                                                                        #
# Networks Fundamentals                                                  #
#                                                                        #
# File Transfer Application -- Implemented Based on FTP Specification    #
# (RFC 959)                                                              #
#                                                                        #
##########################################################################

"""Importing modules"""
import os
import socket
from time import sleep

"""Declaring global variables"""
IP = socket.gethostbyname(socket.gethostname())
PORT = 21
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_DATA_PATH = "serverFiles"
WRKDIR = os.getcwd()
CLIENT_DATA_PATH = "\\clientFiles\\"

def main():
    # Making a client socket connection
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    #While loop enabling clients to send Command and argument to Server.
    while True:
        msg = client.recv(SIZE).decode(FORMAT)
        print(msg)
        msg = input("> ")
        msg = msg.split(" ")
        cmd = msg[0].upper()
        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "QUIT":
            client.send(cmd.encode(FORMAT))
            recv_msg = client.recv(SIZE).decode(FORMAT)
            print(recv_msg)
            break
        elif cmd == "ACCT":
            client.send(f"{cmd} {msg[1]} {msg[2]}".encode(FORMAT))
        elif cmd == "USERNAME":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "PORT":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))

            recv_msg = client.recv(SIZE).decode(FORMAT)
            print(recv_msg)
            retrieve_msg = recv_msg.rstrip().split(" ")
            #print(retrieve_msg)
            retrieve_msg_IP = retrieve_msg[3]
            retrieve_msg_Port = retrieve_msg[4]
            print(retrieve_msg_IP)
            print(retrieve_msg_Port)
            data_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_conn.connect((retrieve_msg_IP,int(retrieve_msg_Port)))
            sleep(5)
            data_conn.close()
        elif cmd == "RETR":
            #Selecting a Passive connection as its the default mode
            client.send(f"PASV".encode())
            #Receiving from Server in order to download
            recv_msg = client.recv(SIZE).decode(FORMAT)
            print(recv_msg)
            retrieve_msg = recv_msg.rstrip().split(" ")
            #print(retrieve_msg)
            retrieve_msg_IP = retrieve_msg[4]
            retrieve_msg_Port = retrieve_msg[5]
            #print(retrieve_msg_IP)
            #print(retrieve_msg_Port)
            data_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_conn.connect((retrieve_msg_IP,int(retrieve_msg_Port)))

            filename = msg[1]
            print("150 Opening file data connection \n")
            client.send(f"{cmd} {filename}".encode())
            #data_conn.send("A string".encode())
            path = WRKDIR + CLIENT_DATA_PATH
            new_path = path + str(filename)
            print (new_path)
            data_msg = data_conn.recv(8192).decode()
            #Writing to the local folder client_data
            file = open(new_path,"w")
            while data_msg:
                file.write(data_msg)
                print('file is uploading...')
                data_msg = data_conn.recv(8192).decode()
            #Closing connection and file
            file.close()
            data_conn.close()
        elif cmd == "STOR":
            #Uploading information from the client side
            client.send(f"PASV".encode())
            recv_msg = client.recv(SIZE).decode(FORMAT)
            retrieve_msg = recv_msg.rstrip().split(" ")
            retrieve_msg_IP = retrieve_msg[4]
            retrieve_msg_Port = retrieve_msg[5]
            data_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_conn.connect((retrieve_msg_IP,int(retrieve_msg_Port)))
            filename = msg[1]
            #Enabling new connection to store on another port
            print("150 Opening file data connection \n")
            client.send(f"{cmd} {filename}".encode())
            path = WRKDIR + CLIENT_DATA_PATH
            new_path = path + str(filename)
            file = open(new_path,"r")
            file_content = file.read(8192)
            while file_content: 
                data_conn.send(file_content.encode())
                file_content = file.read(8192)

            client.send(f"NOOP".encode())
            file.close()
            data_conn.close()    
        elif cmd == "DELE":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "USER":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "PASS":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "NOOP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "TYPE":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "STRU":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "CWD":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "CDUP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "PWD":
            client.send(cmd.encode(FORMAT))
        elif cmd == "MODE":
            client.send(f"{cmd} {msg[1]}".encode(FORMAT))
        elif cmd == "PASV":
            client.send(cmd.encode(FORMAT))
        else :
            client.send(f"{cmd}".encode(FORMAT))

    client.close()
    
if __name__ == "__main__":
    main()