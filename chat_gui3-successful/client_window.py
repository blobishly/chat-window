import socket
import threading
from chat_widget import ChatWidget
from time import sleep, time

class ChatClient:
    
    def __init__(self):
        self.chat_widget = ChatWidget(Title="Client Window")
        self.chat_widget.add_message("Welcome!")
        self.My_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = "client"
        
        
        
    def Win_active(self):
        '''returns wether or not the window of this server is active'''
        try:
            return self.chat_widget.check_exists()
        except: return False
        
        
    
    def conncet_to_server (self,host:str, port:int):
        '''connect to a server using host ip and port no', returns true and shows a message if successful'''
        self.Server_host = host
        self.Server_port = port
        self.My_socket.settimeout(10)
        
        try:
            self.My_socket.connect((self.Server_host, self.Server_port))
            if (is_socket_connected(self.My_socket)):
                self.chat_widget.add_message("Connected To server!")
                sleep(0.1)
                self.send_message("@"+self.username)
                return True
            else:
                self.chat_widget.add_message("connection Failed")
                return False
        except:
            return False
        
    def connect_to_server_user_imput (self):
        '''accept IP adress and port no' from user and connect according to them'''
        try:
            self.chat_widget.add_message("Enter username:")
            self.username=self.chat_widget.get_next_message()
            self.chat_widget.add_message("Enter host:")
            self.host=self.chat_widget.get_next_message()
            self.chat_widget.add_message("Enter port:")
            self.port=int(self.chat_widget.get_next_message())
            if (not self.conncet_to_server(self.host,self.port)):
                self.connect_to_server_user_imput()
        except: 
            #print("conncet user imput closed")
            return
        

    
    
    def receive_a_message(self, My_socket : socket.socket):
            '''accepts the next messege from the connected server, returns it, and displays it'''
            try: 
                message = My_socket.recv(1024).decode('utf-8')
                if (message and message[0]!="@"):
                    self.chat_widget.add_message(message)
                    return message
                else: return self.receive_a_message(My_socket)
            except:
                #print("receive massage closed")
                return None
                
    def open_for_incoming(self): 
        ''''wait until connected to a server, then wait for any INCOMING messages from the server and show them'''
        try:
            while (not is_socket_connected(self.My_socket)):
                sleep(0.5)
                if (not self.Win_active):
                    #print("open for messages cloesd")
                    return
                
            self.chat_widget.add_message("open for incoming messages")
            
            while (self.Win_active and is_socket_connected(self.My_socket)):
                message = self.receive_a_message(self.My_socket)
                
            return
        except:
            #print("open for messages cloesd")
            return        
    
    
    
    def send_message(self, message : str):
        '''sends a message to the connected server and return if succesful'''
        try:
            self.My_socket.send(message.encode('utf-8'))
            return True
        except: return False         

    def open_to_send(self):
        '''wait until connected to a server, then wait for any ENTERED messages and send them to the connected server'''
        try:
            while (not is_socket_connected(self.My_socket)):
                sleep(0.5)
                if (not self.Win_active):
                    #print("open to send closed")
                    return
            
            if(self.Win_active):    
                self.chat_widget.add_message("open for your messages")
            
            while (self.Win_active):
                message = self.chat_widget.get_next_message()
                self.send_message(message)
                
        except:
            #print("open to send closed")
            return
        


    def Run_Threads(self):
        '''run the threads and close the socket when the window is closed'''
        self.connect_to_server_thread = threading.Thread(target=self.connect_to_server_user_imput)
        self.connect_to_server_thread.start()
        self.open_to_send_thread = threading.Thread(target=self.open_to_send)
        self.open_to_send_thread.start()
        self.open_for_Incoming_thread = threading.Thread(target=self.open_for_incoming)
        self.open_for_Incoming_thread.start()
        self.window_loop_thread = threading.Thread(target=self.chat_widget.mainloop())
        self.window_loop_thread.start()
        
        # after the window is closed:
        self.My_socket.shutdown
        self.My_socket.close



def is_socket_connected(sock :socket.socket):
    '''returns wether or not the socket has a peer'''
    try:
        # This will raise an exception if the socket is not connected
        sock.getpeername()
        return True
    except:
        return False
        

      
def send_message_to_socket(message : str, target:socket.socket):
    '''sends the string to the target socket'''
    target.send(message.encode('utf-8'))



if __name__ == "__main__":
    ins = ChatClient()
    ins.Run_Threads()