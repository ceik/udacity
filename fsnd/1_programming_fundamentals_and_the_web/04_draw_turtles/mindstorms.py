import turtle

def draw_square():
	brad = turtle.Turtle()
	brad.color("yellow")
	brad.shape("turtle")
	brad.speed(20)

	x = 1
	while x < 5:
		brad.forward(100)
		brad.right(90)
		x += 1

def draw_circle():
	angie = turtle.Turtle()
	angie.shape("arrow")
	angie.color("blue")
	angie.speed(2)

	angie.circle(100)

def draw_triangle():
	jack = turtle.Turtle()
	jack.color("yellow")
	jack.shape("turtle")
	jack.speed(2)

	x = 1
	while x < 4:
		jack.forward(100)
		jack.right(120)
		x += 1

def draw_squircle():
	elke = turtle.Turtle()
	elke.color("yellow")
	elke.shape("turtle")
	elke.speed(20)

	for i in range(1, 37):
		for x in range(1, 5):
			elke.forward(100)
			elke.right(90)
		elke.right(10)

def draw_art():
	window = turtle.Screen()
	window.bgcolor("red")

	# draw_square()
	# draw_circle()
	# draw_triangle()
	draw_squircle()

	window.exitonclick()

draw_art()
