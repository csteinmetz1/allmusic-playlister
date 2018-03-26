import os 

if not os.path.isdir("data/"):
	os.makedirs("data/")
	print("Created 'data' directory to hold .csv results.")

if not os.path.isdir("pages/"):
	os.makedirs("pages/")
	print("Created 'pages' directory to hold .html source pages.")

if not os.path.isfile("keys.json"):
	with open("keys.json", "w") as keys_file:
		keys_file.write("""{"client_id" : "YOUR_CLIENT_ID", "client_secret" : "YOUR_CLIENT_SECRET", "redirect_uri" : "http://localhost:8888/callback}""")
	print("Created 'keys.json' file. Make sure to follow README details to set your API keys.")