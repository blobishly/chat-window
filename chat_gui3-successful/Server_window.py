import socket
import threading
from time import sleep, time
from turtle import Turtle
from chat_widget import ChatWidget



class ChatServer:
    
    def __init__(self, port:int):
        self.host = "localhost"
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.client_sockets = []
        self.client_addr=[]
        self.client_names=[]
        self.Threads_For_Clients =[]
        self.close_event = threading.Event()
        self.active=True
        
        self.chat_widget = ChatWidget(Title="Server window")
        self.chat_widget.add_message("Welcome to the chat!")
        ip_address_localhost = socket.gethostbyname('localhost')
        self.chat_widget.add_message("host: " + str(ip_address_localhost) + "\nport: "+ str(self.port))
         
         
         
    def client_name(self, client :socket.socket):
        '''find the name of the client if it was properly registered
        with its name in the name list under the same index as its socket is in the socket list'''
        
        #self.chat_widget.add_message("client name")
        try:
            client_name= self.client_names[self.client_sockets.index(client)]
        except: client_name = "client"
        return client_name
    
    
    
    def connect_a_client(self):
        '''wait for a SINGLE client to connect, then add it to the client list, 
        create a thread that listens for messages from that client, and add that thread to the thread list'''
        
        self.socket.settimeout(10)
        
        try:
            new_client_socket, new_client_address = self.socket.accept()
            
            self.client_names.append(self.receive_a_message(new_client_socket))
            self.client_sockets.append(new_client_socket)
            self.client_addr.append(new_client_address)
            
            self.chat_widget.add_message(f"Client connected")
            
            Listen_to_client_thread = threading.Thread(target=self.Listen_to_client, args=(new_client_socket,))
            self.Threads_For_Clients.append(Listen_to_client_thread)
            Listen_to_client_thread.start()     # the method doesn't proceed and doesn't leave this method from when this line is reached
            #print("we're moving!")
            
            return new_client_socket, new_client_address
        except:
            return self.connect_a_client()
    
    def wait_for_clients(self):
        '''Connect any number of Clients'''
        try:
            self.chat_widget.add_message("open for clients")
            
            while (self.active):
                self.connect_a_client()
                
        except: return       
            
            
    def receive_a_message(self, client_socket: socket.socket):
            '''wait for ONE incoming message from the client socket to this server and display it'''
            
            client_socket.settimeout(10)
            
            try:     
                if(self.active and is_socket_connected(client_socket)):
                    
                    message = client_socket.recv(1024).decode('utf-8')
                    client_name=self.client_name(client_socket)
                    if (message!=None):
                        if (message[0]!="@"):
                            self.chat_widget.add_message(f"{client_name}: {message}")
                        return message
                    else: return self.receive_a_message(client_socket)   
            except(socket.timeout):
                return self.receive_a_message(client_socket)
            
            return None
            
    def Listen_to_client(self,client_socket:socket.socket):
        '''wait for ONE client to send messages and display them'''
        
        self.chat_widget.add_message("open for incoming messages")
        client_name=self.client_name(client_socket)
        
        try:
            while (self.active and is_socket_connected(client_socket)):
                
                message = self.receive_a_message(client_socket)
                if (message !=None and message[0]!="@"):
                    self.Send_to_all(str(message),client_socket,client_name)
                    
                if (not is_socket_connected(client_socket)):
                    self.chat_widget.add_message(f"client disconnected")
                    return
        except: return
    
    
    
    def Send_to_all(self, message:str, exceptioned=None, sender ="server"):
        '''send a SINGLE message to all clients connected to this server except the one who's socket is exceptioned'''
        
        if (not (message==None or message.isspace())):
            for client_socket in self.client_sockets:
                if (exceptioned is None or client_socket != exceptioned):
                    
                    send_message_to_socket(sender+": "+str(message), client_socket)
                
    def open_to_send(self):
        '''wait for any number of messages ENTERED to the window and send them to all clients connected to the server'''
        
        self.chat_widget.add_message("Open for your messages")  
        
        while (self.active):
            try:
                message = self.chat_widget.get_next_message()
                self.Send_to_all(message)
            except:
                return


    def Track_active(self):
        '''wait until the window is open, then until closed, then terminate the socket and set self.active to False'''
        while(not self.chat_widget.check_exists): sleep(0.5)
        
        while(self.chat_widget.check_exists): sleep(0.5)
        
        self.active=False
        self.close_event.set()
        self.socket.shutdown
        self.socket.close


    def Run_Threads(self):
        '''run the threads'''
        
        self.chat_server_thread = threading.Thread(target=self.wait_for_clients)
        self.chat_server_thread.start()
        self.open_to_send_thread = threading.Thread(target=self.open_to_send)
        self.open_to_send_thread.start()
        self.Track_active_thread = threading.Thread(target=self.Track_active)
        self.Track_active_thread.start()
        self.window_loop_thread = threading.Thread(target=self.chat_widget.mainloop())
        self.window_loop_thread.start()
        
        
        



def is_socket_connected(sock :socket.socket):
    '''returns wether or not the socket has a peer'''
    
    try:
        # This will raise an exception if the socket is not connected
        peername = sock.getpeername()
        return True
    except (socket.error, OSError):
        return False
      
      
      
def send_message_to_socket(message : str, target:socket.socket):
    '''sends the string to the target socket, returns wether or not it succeeded'''
    
    try:
        target.send(message.encode('utf-8'))
        return True
    except: return False



if __name__ == "__main__":
    ins = ChatServer(1234)
    ins.Run_Threads()