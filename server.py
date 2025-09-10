##########################################################################
#                                                                        #
# Mhlengeni Miya                                                         #
#                                                                        #
# ELEN4017 -- Networks Fundamentals                                      #
#                                                                        #
# File Transfer Application -- Implemented Based on FTP Specification    #
# (RFC 959)                                                              #
#                                                                        #
##########################################################################

# server.py

"""Importing modules"""
import socket
import threading
import os
import random

"""Declaring global variables"""
IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 21
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_DATA_PATH = "\\serverFiles\\"


"""server class"""
# Creating a FTP Server class with multiple threads capability
class Server (threading.Thread):
    """A server class with basic functionality and some added functionalities."""
    def __init__(self, connection, addr):
        """Initialize Server's attributes."""
        threading.Thread.__init__(self) # Inherit all the methods of the super class
        self.connection = connection
        self.addr = addr
        self.data_conn = None
        self.type = None
        self.cwd = os.getcwd()
        self.isUserValid = False
        self.loggedIn = False
        self.threadUsername = ""
        self.threadPassword = ""
        self.stru = 'F'
        self.users = ["mhlengeni"] # To be used in filezilla
        self.passwords = ["miya1991"] # To be used in filezilla

    def sendMessage(self, msg):
        self.connection.send((msg + '\r\n').encode())

    def run(self):
        #Printing the IP and Port to demonstrate a new connection being made
        print(f"[NEW CONNECTION] {self.addr} connected.")

        # Sending welcome message to client
        welcomeMessage = self.welcomeMessage()
        self.sendMessage(welcomeMessage)

        # While loop permitting the exchange between Client Command and Server FTP
        #Protocol response
        sentinel = 0
        while sentinel <= 1:
            # Receiving of client data input determining the command and argument
            data = self.connection.recv(SIZE).decode()
            (f"[SERVER] received : {data}")
            data = data.split(" ")

            cmd = data[0]

            print(f"[SERVER] command received: {cmd}")

            cmd = cmd.rstrip()
            
            if cmd == "HELP":
                message = self.help()
                self.connection.send((message + '\r\n').encode())
            elif cmd == "PORT":
                port = data[1]
                message = self.port(port, self.connection)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "ACCT":
                username = data[1]
                password = data[2]
                message = self.register(username, password)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "USER":
                username = data[1]
                message = self.username(username)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "PASS":
                password = data[1]
                message = self.password(password)
                self.connection.send((message + '\r\n').encode())  
            elif cmd == "PWD":
                message = self.pwd()
                self.connection.send((message + '\r\n').encode()) 
            elif cmd == "CDUP":
                message = self.cdup()
                self.connection.send((message + '\r\n').encode())    
            elif cmd == "QUIT":
                message = self.quit()
                self.connection.send((message + '\r\n').encode())
                self.loggedIn = False
                break
            elif cmd == "LIST":
                message = self.FTP_LIST()
                self.connection.send((message + '\r\n').encode())
            elif cmd == "STOR":
                name = data[1]
                message = self.FTP_STOR(name)
            elif cmd == "DELE":
                filename = data[1]
                message = self.FTP_DELE(filename)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "NOOP":
                message = self.NOOP()
                self.connection.send((message + '\r\n').encode())
            elif cmd == "PASV":
                # Not implemented to be called as a command but within a command
                self.FTP_PASV(self.connection)
            elif cmd == "TYPE":
                type = data[1]
                message = self.FTP_TYPE(type)
                self.connection.send((message + '\r\n').encode())
            # Has a exit error with Filezilla
            elif cmd == "STRU":
                #We are not implementing structure we just
                # Automatically defining it as F
                structure = data[1]
                print(structure)
                message = self.FTP_STRU(structure)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "MODE":
                mode = data[1].upper()
                message = self.FTP_MODE(mode)
                self.connection.send((message + '\r\n').encode())
            elif cmd == "CWD":
                path = data[1]
                message = self.FTP_CWD(path)
                self.connection.send(message.encode())
            elif cmd == "RETR":
                filename = data[1]
                message = self.FTP_RETR(filename)
            # If command entered wrong 
            else:
                message = "502 Command " +cmd+ " not implemented."
                self.connection.send((message + '\r\n').encode())
            print(f"[SERVER] ***************************************************")
        print(f"[SERVER] Client: {self.addr} disconnected")

    def NOOP(self):
        if self.loggedIn:    
            message = "200 OK"
        else:
            message = "530 Not logged in."

        return message

    def welcomeMessage(self):
        message = "220 Welcome to the server. Run command ACCT <yourusername> <yourpassword> to create a new account."

        return message

    def help(self):
        message = "214 help information:\n"
        message += "ACCT <yourusername> <yourpassword>: Create your user account.\n"
        message += "USER <yourusername>: User identification username, first command for logging in.\n"
        message += "PASS <yourpassword>: Takes the user's password, completes user's identification.\n"
        message += "CWD <path>: Change working directory to the selected path.\n"
        message += "CDUP: Change to parent directory, server files directory in this case.\n"
        message += "QUIT: Terminate user, close control connection.\n"
        message += "TYPE <A|E>: Enter type for data transfer. \n"
        message += "STRU <F>: Enter structure for data transfer. \n"
        message += "MODE <S>: Enter mode for data transfer. \n"
        message += "RETR <path>: Download file on the path.\n"
        message += "STOR <path>: Store the data as a file at a server site.\n"
        message += "DELE <filename>: Delete file specified in the pathname from the server site.\n"
        message += "PWD: Returns the name of the current working directory in the reply.\n"
        message += "LIST: Returns a list of files in the current working directory.\n"
        message += "PORT <host,port>: host(h1,h2,h3,h4), port (p1,p2) data connection address.\n"
        message += "PASV: Connect to server data port which is not a default server data port."
        
        return message

    def register(self, username, password):
        # create a text file to store user details if it does not exist in the directory
        if not os.path.exists("username_password.txt"):
            file = open("username_password.txt", "w") # open the file in write mode
            file.close()

        if username in open("username_password.txt", "r").read():
            message = "553 Username not available, try another one."
            return message

        file = open("username_password.txt","a")
        file.write(username)
        file.write(" ")
        file.write(password)
        file.write("\n")
        file.close()

        message = "332 Successfully registered."

        return message

    def username(self, username):
        print(f"The entered username is: {username}")
        new_username = username.rstrip()
        counter = 0
        numberOfUsers = len(self.users)
        for u in self.users:
            if u == new_username:
                self.isUserValid = True
                self.threadUsername = username
                message = "331 User name okay, need password."
                print("True")
                break
            elif u != new_username:
                counter = counter + 1
            elif counter == numberOfUsers:
                self.isUserValid == False
                message = "332 Need account for login."+username+" not registered."
                print("False")

        if not self.isUserValid:
            for line in open("username_password.txt","r").readlines(): # Read the lines
                registeredUsername = line.split() # Split on the space, and store the results in a list of two strings
                if username == registeredUsername[0]:
                    self.threadUsername = username
                    self.isUserValid = True
                    message = "331 User name okay, need password."
                else:
                    message = "332 Need account for login."+username+" not registered."
                print(self.threadUsername)

        return message

      #FTP PASS functionality, determining validity of Client's Password
    def password(self, password):
        new_password = password.rstrip()
        counter = 0
        numberOfPass = len(self.passwords) # get the number of elements in the list
        if self.isUserValid:
            for p in self.passwords:
                if p == new_password:    
                    self.loggedIn = True
                    message = "230 Loggin successfully .\n"
                    break
                elif p != new_password:
                    counter = counter + 1
                elif counter == numberOfPass:
                    self.loggedIn == False
                    message = "530 incorrect password for "+self.threadUsername+".\n" 
                    break

        if not self.loggedIn and self.isUserValid:
            for line in open("username_password.txt","r").readlines(): # Read the lines
                userInfo = line.split() # Split on the space, and store the results in a list of two strings
                if self.threadUsername == userInfo[0] and password == userInfo[1]:
                    message = "230 User logged in, proceed."
                    self.loggedIn = True
                    break
                else:
                    message = "530 Not logged in. Incorrect password."

        return message

    def quit(self):
        message = "221 Logged out."
        return message

    def pwd(self):
        return self.cwd

    def cdup(self):
        """Change current working directory to home directory"""
        mypath = self.cwd + SERVER_DATA_PATH

        if self.loggedIn:
            if os.path.exists(mypath):
                self.cwd = mypath
                message = f"250 Requested file action okay, completed. New working directory is: {mypath}"
            else:
                message = f"550 Requested action not taken, parent directory {mypath} not available."
        else:
            message = "530 Not logged in.\n"

        return message

    def port(self, myPort, connection):
        IP_Port = myPort.split(",")
        indices = [0,1,2,3] # To extract the IP address
        IP_addr = ".".join([IP_Port[i] for i in indices])
        port = int(IP_Port[4])*256 + int(IP_Port[5])

        self.data_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Enables the reuse of address/port
        self.data_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the server port to the comming socket
        print(port)
        self.data_conn.bind((IP_addr, port))
        self.data_conn.listen()
        try:
            Server_Addr = (IP_addr, port)
            print(f"[NEW SERVER] NEW CONNECTION {Server_Addr}")
            connection.send(f"125 Connection established {IP_addr} {port}".encode())
            return
        except:
            print("[SERVER] 425 Error in the passive connection")
            return

    def FTP_PASV(self, connection):
        # Passive mode, not fully usable.
        first_Port_byte = random.randint(20, 230)
        second_Port_byte = random.randint(0, 255)
        Server_Port = (256*first_Port_byte)+second_Port_byte
        Server_IP = socket.gethostbyname(socket.gethostname())
        self.data_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Enables the reuse of address/port
        self.data_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the server port to the comming socket
        self.data_conn.bind((Server_IP,Server_Port))
        self.data_conn.listen()
        try:
            Server_Addr = (Server_IP,Server_Port)
            print(f"[NEW SERVER] NEW CONNECTION {Server_Addr}")
            connection.send(f"227 Passive mode established {Server_IP} {Server_Port}".encode())
        except:
            print("[SERVER] 425 Error in the passive connection")

    #FTP List command functionality not Implemented according to rfc959
    def FTP_LIST(self):
        # Obtaining current directory and performing in built list functionality
        if self.loggedIn:
            files = os.listdir(self.cwd)
            if len(files) == 0:
                send_data = "450 directory is empty.\r\n"
            else:
                send_data = "\n".join(f for f in files)
        else :
            send_data = "530 Not logged in.\n"         
        print(f"[SERVER] {send_data}")
        return send_data  
    # FTP CWD Functionality to change directories
    def FTP_CWD(self,path):
        # Removing unwanted strangents to the variable so as to be able
        # To compare and use its content
        new_path = path.rstrip()
        # Making a new current working directory
        cwd = self.cwd + "\\" + str(new_path)
        if self.loggedIn:
            # Let us check if the path exists
            if os.path.exists(cwd): 
                self.cwd = cwd
                message = "250 Ok, working directory changed. \n"
                print(message)
            else: 
                # If the path does not exist print out an error
                message = "450 requested Dir not found. \n"
                print(message)
        else:
            message = "530 Not logged in\n."         
        print(f"[SERVER] {message}")
        return message

    # Functionality not really a need as its default structure is
    # a file and only that was implemented
    def FTP_STRU(self,struc):
        struct = struc.rstrip()
        if self.loggedIn:
            if struct.upper() == "F":
                send_data = "200 Type chosen is a File type"
                self.stru = 'F'
            else:
                send_data = "501 Syntax error, argument not implemented\n"
        else:
            send_data = "530 Not logged in\n."         
        print(f"[SERVER] {send_data}")
        return send_data
    #Similarly to STRU mode default value is S, for STREAM as
    # Block sizes implementation are difficult.
    def FTP_MODE(self,mode):
        mode = mode.rstrip()
        if self.loggedIn:
            if mode == "S":
                send_data = "200 STREAM mode chosen. \n"
            else:
                send_data = "501 Syntax error, argument not implemented\n"
        
        return send_data
    # Type for Data connection
    def FTP_TYPE(self, type):
        type = type.rstrip()
        if self.loggedIn:
            if type.upper() == "A":
                send_data = "200 ASCII type selected. \n"
                print(send_data)
                # Type is ASCII
                self.type = "A"
            elif type.upper() == "E":
                send_data = "200 EBCDIC type selected. \n"
                print(send_data)
                #Type is Binary
                self.type = "I"
            else:
                send_data = "501 Syntax error, type argument not implemented. \n"
                print(send_data)
        else:
            send_data = "530 Not logged in\n."         
        print(f"[SERVER] {send_data}")
        
        return send_data

    def FTP_DELE(self,filename):
        # First we need to see if it contains any file, if yes we can delete if not
        # we respond accordingly to the client
        filename = filename.rstrip()
        files = os.listdir(self.cwd)
        numFiles = len(files)
        if self.loggedIn:
            print("[SERVER] deleting file....")
            if numFiles == 0:
                send_data = "450 directory is empty. \n"
            else:
                if filename in files:
                    os.remove(f"{self.cwd}/{filename}")
                    # Send message to client that file is deleted
                    send_data = f"250 Ok {filename} deleted. \n"
                    print("[SERVER] File deleted")
                else:
                    send_data = "450 directory NOT found. \n"
        else:
            send_data = "530 Not logged in\n."         
        print(f"[SERVER] {send_data}")
        return send_data


    # Return Function for downloading of files to server
    def FTP_RETR(self,filename):
        # Function needs to be error proned for file directory
        #Did not implement binary
        if self.type == 'I':
            self.type = 'A'
        print(f"filename = {filename}")
        data_conn_socket, data_addr = self.data_conn.accept()
        path = self.cwd + SERVER_DATA_PATH
        new_path = path + str(filename)
        print (new_path)
        #Reading of obtained file
        file = open(new_path,"r") 
        file_content = file.read(8192)
        print(file_content)
        while file_content:
            data_conn_socket.send(file_content.encode())
            file_content = file.read (8192)
        print('[SERVER] Completed. Download successful')
        # Closing of data connection and file
        file.close()
        data_conn_socket.close()
        self.connection.send("Download successful.\n".encode())
   

    # Uploading from the Server.
    def FTP_STOR(self,filename):    
        print("[SERVER] 150 Opening file data connection \n")
        print(f"[SERVER] The filename is {filename}")
        data_conn_socket, data_addr = self.data_conn.accept()
        data_msg = data_conn_socket.recv(8192).decode()
        path = self.cwd + SERVER_DATA_PATH
        new_path = path + str(filename)
        print (new_path)
        file = open(new_path,"w") 
        #file.write(data_msg)
        while data_msg:
            file.write(data_msg)
            print('[SERVER] file is uploading')
            data_msg = data_conn_socket.recv(8192).decode()
            
        file.close()
        data_conn_socket.close()
        self.connection.send("226 Tansfer complete, upload successfull.\n".encode())
    

def main():
    print("[STARTING] Server is starting...")
    
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(ADDR)
    serverSocket.listen()

    sentinel = 0

    while sentinel < 1:
        print ("[LISTENING] Server is listening...")
        connection, addr = serverSocket.accept()
        thread = Server(connection, addr)
        thread.start()        

if __name__ == '__main__':
    main()
