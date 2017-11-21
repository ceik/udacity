import fresh_tomatoes
import media

toy_story = media.Movie("Toy Story", "A story of boy and his toys come to life",
	"https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Toy_Story.jpg/220px-Toy_Story.jpg",
	"https://www.youtube.com/watch?v=KYz2wyBy3kc")

avatar = media.Movie("Avatar", "A marine on an alien planet",
	"https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
	"https://www.youtube.com/watch?v=5PSNL1qE6VY")

school_of_rock = media.Movie("School of Rock", "Using rock music to learn",
	"https://upload.wikimedia.org/wikipedia/en/thumb/1/11/School_of_Rock_Poster.jpg/220px-School_of_Rock_Poster.jpg",
	"https://www.youtube.com/watch?v=XCwy6lW5Ixc")

ratatouille = media.Movie("Ratatouille", "A rat is a chef in Paris",
	"https://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg",
	"https://www.youtube.com/watch?v=c3sBBRxDAqk")

the_godfather = media.Movie("The Godfather", "Making people offers they can't refuse",
	"https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
	"https://www.youtube.com/watch?v=sY1S34973zA")

apocalypse_now = media.Movie("Apocalypse Now", "If I say its safe to surf this beach, then its safe to surf this beach",
	"https://upload.wikimedia.org/wikipedia/en/c/c2/Apocalypse_Now_poster.jpg",
	"https://www.youtube.com/watch?v=IkrhkUeDCdQ")

movies = [toy_story, avatar, school_of_rock, ratatouille, the_godfather, apocalypse_now]

fresh_tomatoes.open_movies_page(movies)
