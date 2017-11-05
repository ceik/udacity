# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define instances of the class Movie defined
# in media.py. After you follow along with Kunal, make some instances
# of your own!

# After you run this code, open the file fresh_tomatoes.html to
# see your webpage!

# https://www.udacity.com/course/viewer#!/c-nd000/l-4185678656/e-991358856/m-1013629064

import media
import fresh_tomatoes

heat = media.Movie("Heat", ("A group of professional bank robbers start to feel "
    "the heat from police when they unknowingly leave a clue at their latest "
    "heist."), "https://upload.wikimedia.org/wikipedia/en/6/6c/Heatposter.jpg",
    "https://www.youtube.com/watch?v=D4KSCBTSaxE",
    1995, "Michael Mann", ["Robert De Niro", "Al Pacino"])

american_beauty = media.Movie("American Beauty", ("A sexually frustrated "
    "suburban father has a mid-life crisis after becoming infatuated with his "
    "daughter's best friend."),
    "http://ia.media-imdb.com/images/M/MV5BMjM4NTI5NzYyNV5BMl5BanBnXkFtZTgwNTkxNTYxMTE@._V1_SY317_CR0,0,214,317_AL_.jpg",
    "https://www.youtube.com/watch?v=3ycmmJ6rxA8",
    1999, "Sam Mendes", ["Kevin Spacey"])

mulholland_drive = media.Movie("Mulholland Drive", ("After a car wreck on the "
    "winding Mulholland Drive renders a woman amnesiac, she and a perky "
    "Hollywood-hopeful search for clues and answers across Los Angeles in a "
    "twisting venture beyond dreams and reality."),
    "http://ia.media-imdb.com/images/M/MV5BMjM1Njg2ODA4OF5BMl5BanBnXkFtZTgwMDM3Mjc1MDE@._V1_SX214_AL_.jpg",
    "https://www.youtube.com/watch?v=XQ5Q0CHQ0EU",
    2001, "David Lynch", ["Naomi Watts"])

fivehundred_days_of_summer = media.Movie("(500) Days of Summer",
    ("An offbeat romantic comedy about a woman who doesn't believe true love "
    "exists, and the young man who falls for her."),
    "http://ia.media-imdb.com/images/M/MV5BMTk5MjM4OTU1OV5BMl5BanBnXkFtZTcwODkzNDIzMw@@._V1_SX214_AL_.jpg",
    "https://www.youtube.com/watch?v=PsD0NpFSADM",
    2009, "Marc Webb", ["Joseph Gordon-Levitt", "Zooey Deschanel"])

lost_in_translation = media.Movie("Lost in Translation", ("A faded movie star "
    "and a neglected young woman form an unlikely bond after crossing paths in "
    "Tokyo."),
    "http://ia.media-imdb.com/images/M/MV5BMTI2NDI5ODk4N15BMl5BanBnXkFtZTYwMTI3NTE3._V1_SX214_AL_.jpg",
    "https://www.youtube.com/watch?v=W6iVPCRflQM",
    2003, "Sofia Coppola", ["Bill Murray", "Scarlett Johansson"])

the_good_shepherd = media.Movie("The Good Shepherd", ("The tumultuous early "
    "history of the Central Intelligence Agency is viewed through the prism of "
    "one man's life."),
    "http://ia.media-imdb.com/images/M/MV5BMTU5MjExMzA1Nl5BMl5BanBnXkFtZTgwMzIxNzQxMTE@._V1_SY317_CR0,0,214,317_AL_.jpg",
    "https://www.youtube.com/watch?v=S8tdWA5g4Xs",
    2006, "Robert De Niro", ["Matt Damon"])



movies = [heat, american_beauty, mulholland_drive, fivehundred_days_of_summer,
    lost_in_translation, the_good_shepherd]
fresh_tomatoes.open_movies_page(movies)
