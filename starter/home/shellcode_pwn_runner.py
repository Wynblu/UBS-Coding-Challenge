import pwn

io = pwn.process('./shellcode')
with open('./payload_shellcode', 'rb') as f:
    payload = f.read()
    io.send(payload)

output = io.recv().decode('latin-1')

print(output)
