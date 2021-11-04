#If you do not have pwntools installed, run the following command: python3 -m pip install --upgrade pwntools
#https://github.com/morse-talk/morse-talk

from pwn import *
import base64
import morse_talk as mtalk

ENGLISH_TO_MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

# Generate MORSE_TO_ENGLISH from ENGLISH_TO_MORSE
MORSE_TO_ENGLISH = {}
for key, value in ENGLISH_TO_MORSE.items():
    MORSE_TO_ENGLISH[value] = key


def english_to_morse(message):
    morse = []  # Will contain Morse versions of letters
    for char in message:
        if char in ENGLISH_TO_MORSE:
            morse.append(ENGLISH_TO_MORSE[char])
    return " ".join(morse)


def morse_to_english(message):
    message = message.split(" ")
    english = []  # Will contain English versions of letters
    for code in message:
        if code in MORSE_TO_ENGLISH:
            english.append(MORSE_TO_ENGLISH[code])
    return "".join(english)




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
