s = "jmt_j]tm`q`t_j]mpjtf^"
string = ""
string += s[11:]
string += s[:-10]
flag = ''
for c in string:
	flag += chr(ord(c) + 5)

print flag[::-1]
