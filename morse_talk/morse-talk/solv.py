#If you do not have pwntools installed, run the following command: python3 -m pip install --upgrade pwntools
from pwn import *
import base64
import morse_talk as mtalk


#Connect with netcat
io = connect("io.ept.gg", 30023)

#Recieve data
data = io.recvuntil("Are you ready?").decode()
print(data)

#Send data
io.sendline("Yes")

#Recieve empty line then the line containing the question
for i in range(100):
	b = 0
	c = 0
	io.recvline()
	question = io.recvline().decode().strip()
	print(question)

	if "ascii" in question:
		decoded = ""
		ascii = question.split(": ")[1]
		ascii = ascii.split(" ")
		print(ascii)
		for a in ascii:
			a = ascii[b]
			a = int(a)
			b = b+1
			decoded = decoded + chr(a)
		io.sendline(decoded)
		
	#Check if it is a morse question and if so, extract the morse code
	if "morse" in question:
		mors = question.split(": ")[1]
		decoded = mtalk.decode(mors)
		print(decoded)
		io.sendline(decoded)
	
	if "Base64" in question:
		base = question.split(": ")[1]
		io.sendline(base64.b64decode(base))
  
	if "equation" in question:
		eqs = ""
		eq = question.split(": ")[1]
		eq = eq.split(" ")
		print(eq)
		if eq[1] == "+":
			eqs = int(eq[0]) + int(eq[2])
		elif eq[1] == "-":
			eqs = int(eq[0]) - int(eq[2])
		elif eq[1] == "*":
			eqs = int(eq[0]) * int(eq[2])
		elif eq[1] == "/":
			eqs = int(eq[0]) / int(eq[2])
		eqs = int(eqs)
		io.sendline(str(eqs))

	if "hexadecimals" in question:
		hex = question.split(": ")[1]
		hex = bytearray.fromhex(hex).decode("ASCII")
		io.sendline(hex)
		

io.interactive()