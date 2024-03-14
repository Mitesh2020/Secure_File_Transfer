import socket
import tqdm
from Crypto.Cipher import AES

key = b"MiteshRathod2002"
nonce = b"MiteshRathod2024"

cipher = AES.new(key, AES.MODE_EAX, nonce)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

file_name = client.recv(1024).decode()
print(file_name)

file_size_bytes = client.recv(1024)
file_size_bytes = file_size_bytes[:-5]  # Remove the last 5 bytes (delimiter)
file_size = int.from_bytes(file_size_bytes, byteorder='big')  # Convert remaining bytes to integer

file = open(file_name, "wb")

done = False
file_bytes = b""

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

while not done:
    data = client.recv(1024)
    if data[-5:] == b"<END>":
        done = True
        data = data[:-5]  # Remove the last 5 bytes (delimiter)
    file_bytes += data
    progress.update(len(data))

file.write(cipher.decrypt(file_bytes))

file.close()
client.close()
server.close()
