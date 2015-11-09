# Lesson 4.4: Dictionaries

# Dictionaries are another crucial data structure to learn in Python in addition to lists.
# These data structures use string keywords to access data rather than an index number in lists.
# Using string keywords gives programmers more flexibility and ease of development to use a
# string keyword to access an element in this data structure.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4181088694/m-3919578552

# Strings vs List vs Dictionary Demo
s = "hello"
p = ["alpha",23]
d = {"hydrogen": 1, "helium": 2}

# Replacing values
# s[2] = "a" # Will produce error, comment this line to continue with rest of code execution
p[1] = 999
d["hydrogen"] = 49
d['lithium'] = 3
d['nitrogen'] = 8
d['nitrogen'] = 7

# Accessing items
print s[2]
print p[1]
print d["hydrogen"]
print d

population = {'Shanghai':17.8, 'Istanbul': 13.3, 'Karachi': 13.0, 'Mumbai': 12.5}

elements = {}
elements['H'] = {'name': 'Hydrogen', 'number': 1, 'weight': 1.00794}
elements['He'] = {'name': 'Helium', 'number': 2, 'weight': 4.002602,
    'noble gas': True}

print elements['H']
print elements['He']
print elements['He']['weight']
