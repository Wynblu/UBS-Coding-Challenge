import pwn

io = pwn.process('./stack')
with open('./payload_stack', 'rb') as f:
    payload = f.read()

io.send(payload)
output = io.recv().decode('latin-1')

print(output)
