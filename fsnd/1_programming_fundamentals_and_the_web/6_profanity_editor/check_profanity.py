import urllib

def read_text():
	quotes_file = open("movie_quotes.txt")
	quotes = quotes_file.read()
	print(quotes)
	quotes_file.close
	check_profanity(quotes)

def check_profanity(text_to_check):
	connection = urllib.urlopen("http://www.wdylike.appspot.com/?q="+text_to_check)
	output = connection.read()
	connection.close()
	
	if output:
		print("Profanity Alert!")
	elif not output:
		print("No curse words.")
	else:
		print("Could not scan the document properly.")

read_text()