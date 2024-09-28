import pwn

io = pwn.process('./crackme')
with open('./payload_crackme', 'r') as f:
    payload = f.read()

io.send(payload)
output = io.recvall().decode('latin-1')

print(output)
