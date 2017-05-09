try:
	import urllib.request
	import ssl
	from bs4 import BeautifulSoup
	import random
	import sys

	def get_it(link, name):
		content = []
		context = ssl._create_unverified_context()
		webpage = urllib.request.urlopen(link, context=context)
		html_doc = webpage.read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		toText = open(str(name) + ".txt", 'w')
		words = soup.get_text().split()

		for word in words:
			if "@" in word:
				content.append(word)

		content = list(set(content))

		for entry in content:
			toText.write(entry + "\n")

		toText.close()
		print("Saved: " + str(name) + ".txt")

	counter = 0

	if len(sys.argv) > 1:
  	  path = sys.argv[1] 
	else:
		path = input("Path or URL:\n")

	if (path[0:4] == "http"):
		get_it(path, counter)
	else:
		content = open(path, 'r')
		for line in content:
			get_it(line, counter)
	counter = counter + 1

except ModuleNotFoundError:
	print("Error importing dependencies.\nMake sure the needed modules are installed, then try again.")
	sys.exit()

except IOError:
	print("Error reading/writing to file.\nPlease try again.")
	sys.exit()

except:
	print("Unknown error occurred.\nPlease try again.")
	sys.exit()
