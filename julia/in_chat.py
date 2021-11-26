import random

def chat(input_text):
	user_message = str(input_text).lower()
	Emot = ['🙄', '😑', '😘', '😴', '🤕', '😵', '😎', '🤒', '😪', '😬', '😱', '😈','👿', '😩', '😤', '😫', '🤗', '😟', '😍', '🤔', '😀', '😃', '😄', '😊', '🙂', '😉', '🙃', '😆', '😅', '😂', '😗', '😜', '😛', '😍', '😘', '😋','☺️', '😙', '😚', '😉', '🙃']
	Emoji = random.choice(Emot)
	if user_message in ("hi", "eyy", "oi", "hey", "hello", "alo", "allo", "hai", "halo"):
		resp = random.choice(["uyy paan?", "ada apa nich?", "iya?", "hai juga 😑", "hello", "Eh", "eyy"])
		respon = (resp + " " + Emoji)
		return respon

	elif user_message in ("lu saha? ", "kamu siapa?", "u cp y", "siapa?", "bot?","siapa","saha", 'siapa','saha', 'ini saha', 'ini siapa'):
		y = "Coba deh tanya @ini_peninggi_badan"
		x = y + " " + Emoji
		return x

	elif 'ping' == user_message:
		return Emoji

	elif user_message in ('ka', 'mal','ika','malika','ik','bot','malik','sayang','yang','beb'):
		x = 'yoi' +' '+ Emoji
		return x
		
	elif user_message in ('gass ga?', 'ntar malem gas?', 'gas?', 'gas ga?', 'ntar malem?', 'ntar malam?'):
		x = ['gass! ', 'ok beb', 'gasss', 'gas! ', 'awkay']
		y = random.choice(x)
		return y

	elif user_message in ('/note', '???', 'p', 'P', 'pppp', 'pepepe', 'pepe', 'q', 'r', 's'):
		return 'mau typing apa?'