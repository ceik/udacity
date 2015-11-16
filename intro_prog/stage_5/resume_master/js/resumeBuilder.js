/*
This is empty on purpose! Your code to build the resume will go here.
 */

var firstName = "chris"
var age = 32
var email = "chris@udacity.com"
var newEmail = email.replace("udacity", "gmail")
var fullName = "Christian Eik"
var role = "Data Analytics"

console.log(firstName)
console.log(email)
console.log(newEmail)

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

bio.city = "Singapore"
bio["education"] = "Goethe University Frankfurt"

$("#main").append(bio.name);
$("#main").append(bio.city);
$("#main").append(bio.education);
