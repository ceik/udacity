// JavaScript Reference & Tutorial:
// https://developer.mozilla.org/en-US/docs/Web/JavaScript

var firstName = "chris"
var age = 32
var email = "chris@udacity.com"
var newEmail = email.replace("udacity", "gmail")
var fullName = "Christian Eik"
var role = "Data Analytics"

// This print stuff to the console (can be viewed by inspect element in browser)
// console.log(firstName)
// console.log(email)
// console.log(newEmail)

var formattedName = HTMLheaderName.replace("%data%", fullName);
var formattedRole = HTMLheaderRole.replace("%data%", role);

$("#header").prepend(formattedRole);
$("#header").prepend(formattedName);

var skills = ["programming", "python", "standing on one leg"]

$("#main").append(skills);
$("#main").append(skills[0]);
$("#main").append(skills.length);

var bio = {
    "name" : "Chris",
    "age" : 32,
    "skills" : skills
}

// The following two are ways to add to an object.
bio.city = "Singapore"
bio["education"] = "Goethe University Frankfurt"

$("#main").append(bio.name);
$("#main").append(bio.city);
$("#main").append(bio.education);

var education = {
    "schools": [
        {
            "name": "Allgemeines Gymnasium Lohne",
            "city": "Lohne, Germany",
            "degree": "Abitur",
            "major": ["Political Science", "Biology", "History"]
        },
        {
            "name": "Goethe University Frankfurt",
            "city": "Frankfurt am Main, Germany",
            "degree": "BSc",
            "major": ["Economics"]
        }
    ]
}

// http://jsonlint.com/ can be used to validate JSON syntax
