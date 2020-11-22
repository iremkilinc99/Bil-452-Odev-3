import socket
import ssl
from asn1crypto import x509
import sys
port = int(sys.argv[1]) #int(input("Port giriniz: "))
host = ""   # Get local machine name
server_cert = 'server.crt'
server_key = 'server.key'
client_cert = 'client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_cert)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(5)

print('Server listening....')

while True:

    conn, addr = serverSocket.accept()     # Establish connection with client.
    print("Client connected : {} : {} ".format(addr[0], addr[1]))
    connection = context.wrap_socket(conn , server_side = True,)
    print("SSL Establieshed My Darling. Peer: {} ".format(connection.getpeercert()))
    print(" ")
    print(repr(connection.getpeername()))
    d = connection.getpeercert(binary_form=True)

    print(connection.cipher())
    cert = x509.Certificate.load(d)
    print(cert.public_key.unwrap())
    c = connection.getpeercert();

    if not c or ('commonName', 'iremtos') not in c['subject'][5]:
        raise ssl.CertificateError
        conn.close()


    filename = 'o.txt' #istedigin dosyayi gir

    f = open(filename, 'r')
  #  data = connection.recv(2048)
    l = f.read(2048)

    try:

        while (l):
            l = bytes(l)
            connection.send(l)
            #print('Sent ', repr(l))
            l = f.read(1024)

        connection.send(b'bitti')
    except ssl.SSLError as e:
        print(e)

    finally:
        print('Done sending')
        f.close()
      #  connection.send(b"Seni cok ozledim be irem...")
        conn.close()
        print('Thank you for connecting motherfucker.')
