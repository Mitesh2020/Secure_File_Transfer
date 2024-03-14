import os
import socket
from Crypto.Cipher import AES

key = b"MiteshRathod2002"
nonce = b"MiteshRathod2024"

cipher = AES.new(key, AES.MODE_EAX, nonce)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

file_size = os.path.getsize("coc.exe")

with open("coc.exe", "rb") as f:
    data = f.read()

encrypted = cipher.encrypt(data)

# Send file name and size
client.send("coc.exe".encode())
client.sendall(file_size.to_bytes(1024, byteorder='big'))  # Send file size as binary data
client.sendall(encrypted)
client.send(b"<END>")

client.close()
