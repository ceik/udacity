# Lesson 3.3: Use Classes
# Mini-Project: Check Profanity

# Typos can be embarassing! Imagine how you'd feel if you
# accidentally sent your boss an email that said "I'll take
# a sh!t at it" instead of "I'll take a shot at it". Write
# a program that can detect curse words in a string of text.

# Use this space to describe your approach to the problem.
#
#
#
#

import urllib

def read_text():
    quotes = open("movie_quotes.txt", "r")
    contents_of_file = quotes.read()
    print(contents_of_file)
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(text_to_check):
    conn = urllib.urlopen(
        "http://www.wdyl.com/profanity?q=" + text_to_check)
    output = conn.read()
    conn.close()
    if "true" in output:
        print("Profanity Alert!!")
    elif "false" in output:
        print("Thid document is clean.")
    else:
        print("Could not scan document properly.")

read_text()
