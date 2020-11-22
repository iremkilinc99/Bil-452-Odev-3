import socket
import ssl
import time
import sys

from asn1crypto import x509

ip = sys.argv[1] #input ("Ip giriniz: ")
port = int(sys.argv[2]) #int(input("Port giriniz: ") )

server_sni_hostname = 'iremtos'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile = server_cert)
context.load_cert_chain(certfile=client_cert,keyfile=client_key)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(clientSocket,server_side= False, server_hostname=server_sni_hostname)
start = time.time()
conn.connect((ip,port))

d = conn.getpeercert(binary_form=True)
filename = sys.argv[3] #input("Dosya ismini giriniz: ")
conn.send(b'filename')
cert = conn.getpeercert();

if not cert or ('commonName', 'iremtos') not in cert['subject'][5]:
    raise ssl.CertificateError
    clientSocket.close()


print(conn.getpeername())
print(conn.cipher())
cert = x509.Certificate.load(d)
print(cert.public_key.unwrap())
print(conn.getpeercert())
try :
    with open(filename+str('_alindibabacim;)'), 'w') as f:
        while True:
            data = conn.recv(2048)
            if(data != b'bitti'):
                data = data.decode("utf-8")
               # print(data)
                f.write(data.encode("utf-8"))
            else :
                break
                print("Finished")

finally:
    end = time.time()
    time = end - start
    print('Successfully ended the connection')
    clientSocket.close()
    print('connection closed')
    print('time',time)