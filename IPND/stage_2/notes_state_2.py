# Lesson 2.1: Introduction to Serious Programming

# Programming is grounded in arithmetic, so it's important
# to know how programming languages do simple math.
# Thankfully, Python follows the same math rules people do.
# See if you can predict the output of this code.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4180729266/m-48652460

print 3
print 1 + 1

# Add your own code and notes here

# Computer: Universal machine that can be programmed to to any kind of
#           computation. Has a few basic instructions preprogrammed.
# Program: Percise sequence of steps. Combine basic instructions of the computer
#          to do something useful.

# Quiz 1
print 7 * 7 * 24 * 60

# Ambiguity: Natural languages are highly ambiguous. Programming languages can
#            not be ambiguous. E.g. the word biweekly can mean twice a week or
#            once every two weeks
#
# Verbosity: Natural languages are very verbose. Programming languages avoid
#            this because it makes the code and coding itself more efficient.
#
# Grammar: E.g. natural languages have sentence structure: Subject - Verb -
#          Object. Programming languages are defined in a similar way.
#
# Backus-Naur Form: Way to define syntax in a programming language.
#                   <Non-Terminal> -> Replacement. This is being repeated until
#                   you end up with only terminals
#
# Derivation: Starting from a non-terminal and following the rules to derive
#             a sequence of terminals. For example:
# Sentence -> Subject Verb Object
# Subject -> Noun
# Noun -> "I"
# Verb -> "like"
# Object -> Noun
# Noun -> "cookies"

# Python grammar for arithmetic expressions:
#     Expression -> Expression Operator Expression
#     Expression -> Number
#     Expression -> (Expression)
#     Operator -> +
#     Operator -> *
#     Number -> 0, 1, ... (actual rule is quite complicated)
#
# This was a recursive definition, you can insert the first definition of
# expression into itself infinitely often.

# Quiz 2

speed_of_light = 299792458
centimeters = 100
nanosecond = 1.0 / 1000000000

print speed_of_light * centimeters * nanosecond





# Lesson 2.2: Variables

# Programmers use variables to represent values in their code.
# This makes code easier to read by telling others what values
# mean. It also makes code easier to write by cutting down on
# potentially complicated numbers that repeat in our code.

# We sometimes call numbers without a variable "magic numbers"
# It's best to reduce the amount of "magic numbers" in our code

# https://www.udacity.com/course/viewer#!/c-nd000/l-4192698630/m-48660987

speed_of_light = 299792458.0
billionth = 1.0 / 1000000000.0
nanostick = speed_of_light * billionth * 100
print nanostick

# Add your own code and notes here

# Assignment Statement:
#     Name = Expression
# In python (and many other languages) the = means assignment (not equal)

# Quiz 1
speed_of_light = 299792458.0
cycles_per_second = 2700000000.0
print speed_of_light / cycles_per_second

# Quiz 4
age = 26
age_days = age * 365
print age_days



# Lesson 2.2: Strings

# Strings are sequences of characters that are enclosed in quotes.
# We can enclose them with single or double quotes and assign them
# to variables. We can even combine strings by adding them (we call
# this concatenation).

# https://www.udacity.com/course/viewer#!/c-nd000/l-4192698630/m-48700403

print 'Hello'
print "Hello"

hello = "Howdy"
print hello

# Add your own code and notes here

# String: Sequence of characters between quotes.

print 'hello' + ' sir'
print '!' * 23

# Charaters can be indexed: 'udacity'
#                            0123456
# The format is <string>[<expression>] or <string>[expression:expression] for a
# subsequence.
# The find method returns the first index of the string that is searched for. It
# returns a number, which is -1 if the string is not found. find can also take
# a second parameter that stands for the index where find is supposed to start
# searching.
# Another useful string method is replace:
# string.replace(old, new, max_replacements)
u = 'udacity'
print u[2]
print u[-2]
print u.find('u')
print (u+u).find('u', 3)




# Lesson 2.3: Procedures

# Functions (also known as procedures or methods) take input and return an output.
# Programmers use functions all the time! They may seem confusing at first but
# the more you use and make them, the better you'll get!

# https://www.udacity.com/course/viewer#!/c-nd000/l-4141089439/m-48667860

def rest_of_string(s):
    return s[1:]

print rest_of_string('audacity')

# Add your own code and notes here

# Procedure: <procedure>(<input>, <input>, ...)
# Inputs are sometimes called operands or arguments.




# Lesson 2.4: Making Decisions - If Statements

# We'll often write programs that need to make comparisons between values.
# We can do comparisons just like we do in math with the < and > signs.
# We can also do equality comparisons with != (not equal) and ==.
# Comparisons always return a Boolean value (either True or False).

# https://www.udacity.com/course/viewer#!/c-nd000/l-4196788670/e-48727556/m-48724313

print 2 < 3
print 21 < 3
print 7 * 3 < 21
print 7 * 3 != 21
print 7 * 3 == 21

# Add your own code and notes here


# Lesson 2.4: While Loops

# Loops are an important concept in computer programming.
# Loops let us run blocks of code many times which can be
# really useful when we have to repeat tasks.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4196788670/e-48686708/m-48480488

def count():
    i = 0
    while i < 10:
        print i
        i = i + 1

count()

# Add your own code and notes here



# Lesson 2.6: Structured Data - Lists

# Similar to how strings are seuqences of characters, lists are
# sequences of anything! We can have lists of numbers, lists of
# characters, even lists of lists! And we can mix up the contents
# too so we can have lists containing many different things.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4180729266/m-48652460

p = ['y', 'a', 'b', 'b', 'a', '!']
print p
print p[0]
print p[2:4]

# Add your own code and notes here

# Lists are mutable while strings are not.
# Because of this, whenever a list is mutated inside a function this will
# change the list in the global environment!


# Lesson 2.6: For Loops

# For loops, like while loops, are useful for running a block of code
# multiple times. For loops make iterating through elements in a list
# easier than using a while loop.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4152219158/m-48204891

def print_all_elements(p):
    for e in p:
        print e

myList = [1, 2, [3, 4]]
print_all_elements(myList)

# Add your own code and notes here



# Lesson 2.7: How to Solve Problems - Days Between Dates

# In this lesson, you'll be working on solving a much
# bigger problem than those you've seen so far. If you
# want, you can use this starter code to write your
# quiz responses and then copy and paste into the
# Udacity quiz nodes.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4184188665/m-108325398

# Simple Mechanical Algorithm
# days = 0
# while date1 is before date2:
#     date1 = advance to next day
#     days += 1

# Fill in the functions below to solve the problem.

def isLeapYear(year):
    if year % 4.0 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True

def daysInMonth(year, month):
    daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and isLeapYear(year):
        return 29
    else:
        return daysOfMonths[month - 1]


def nextDay(year, month, day):
    if day < daysInMonth(year, month):
        return year, month, day + 1
    else:
        if month == 12:
            return year + 1, 1, 1
        else:
            return year, month + 1, 1

def dateIsBefore(year1, month1, day1, year2, month2, day2):
    """Returns True if year1-month1-day1 is before year2-month2-day2. Otherwise, returns False."""
    if year1 < year2:
        return True
    if year1 == year2:
        if month1 < month2:
            return True
        if month1 == month2:
            return day1 < day2
    return False

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    """Returns the number of days between year1/month1/day1
       and year2/month2/day2. Assumes inputs are valid dates
       in Gregorian calendar."""
    # program defensively! Add an assertion if the input is not valid!
    assert not dateIsBefore(year2, month2, day2, year1, month1, day1)
    days = 0
    while dateIsBefore(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay(year1, month1, day1)
        days += 1
    return days

def test():
    test_cases = [((2012,1,1,2012,2,28), 58),
                  ((2012,1,1,2012,3,1), 60),
                  ((2011,6,30,2012,6,30), 366),
                  ((2011,1,1,2012,8,8), 585 ),
                  ((1900,1,1,1999,12,31), 36523)]

    for (args, answer) in test_cases:
        result = daysBetweenDates(*args)
        if result != answer:
            print "Test with data:", args, "failed"
        else:
            print "Test case passed!"

test()


# Own code that is more efficient but doesn't factor in start dates in the same
# year/month

daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isLeapYear(year):
    if year % 4.0 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True


def daysBetweenDates(y1, m1, d1, y2, m2, d2):
    days = d2
    days += sum(daysOfMonths[0:m2-1])
    days += (y2 - 1 - y1) * 365
    days +=  daysOfMonths[m1-1] - d1
    days += sum(daysOfMonths[m1:])

    if m1 <= 2:
        start_year = y1
    else:
        start_year = y1 + 1

    if m2 <= 2:
        end_year = y2 - 1
    else:
        end_year = y2

    while end_year >= start_year:
        if isLeapYear(end_year):
            days +=1
        end_year += -1

    return days

print daysBetweenDates(1988, 11, 28, 2015, 11, 2)
