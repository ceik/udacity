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
