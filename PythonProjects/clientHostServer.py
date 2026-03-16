import socket
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = socket.gethostname()
port=5490

soc.bind((ip,port))

soc.listen(10)

def Counter_function(client, client_addr):
    for i in range(1, 5000001):
        client.send(str(i).encode('utf-8'))
try:
    while True:
        client, client_addr = soc.accept() 
        print("Client accepted")
        thread = threading.Thread(target = Counter_function, args=(client,client_addr))
        thread.start()
except:
    print("Successfull")
    client.close()
    soc.close()
