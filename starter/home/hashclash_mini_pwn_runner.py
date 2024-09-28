import pwn

pwn.process(["/usr/bin/chmod", "a+x", "./payload_homework_mini"]).wait()
pwn.process(["/usr/bin/chmod", "a+x", "./payload_malicious_mini"]).wait()
print(pwn.process("./payload_homework_mini").recv().decode("latin-1"))
print(pwn.process("./payload_homework_mini").recv().decode("latin-1"))
homework_hash = (
    pwn.process(["/usr/bin/python3", "mini.py", "./payload_homework_mini"])
    .recv()
    .decode("latin-1")
)
print(homework_hash)
malicious_hash = (
    pwn.process(["/usr/bin/python3", "mini.py", "./payload_malicious_mini"])
    .recv()
    .decode("latin-1")
)
print(malicious_hash)

if malicious_hash.split("= ")[-1].strip() == homework_hash.split("= ")[-1].strip():
    print("hash matches")
    print(pwn.process("./payload_malicious_mini").recv().decode("latin-1"))
else:
    print("hash does not match")
