class Parent():
	def __init__(self, last_name, eye_color):
		print("Parent constuctor called")
		self.last_name = last_name
		self.eye_color = eye_color

	def show_info(self):
		print("Last Name - " + self.last_name)
		print("Eye Color - " + self.eye_color)

# Subclass
class Child(Parent):
	def __init__(self, last_name, eye_color, number_of_toys):
		print("Child constuctor called")
		Parent.__init__(self, last_name, eye_color)
		self.number_of_toys = number_of_toys

# Method Overriding
	def show_info(self):
		print("Last Name - " + self.last_name)
		print("Eye Color - " + self.eye_color)
		print("Number of Toys - " + str(self.number_of_toys))

bill_meyer = Parent("Meyer", "Green")
bill_meyer.show_info()
frank_meyer = Child("Meyer", "Green", 5)
frank_meyer.show_info()