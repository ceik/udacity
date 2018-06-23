
var counter1 = document.getElementById("counter1");
var counter2 = document.getElementById("counter2");
var catPic1 = document.getElementById("cat-pic1");
var catPic2 = document.getElementById("cat-pic2");

function increment1() {
    count = parseInt(counter1.innerHTML)
    counter1.innerHTML = count + 1
}

function increment2() {
    count = parseInt(counter2.innerHTML)
    counter2.innerHTML = count + 1
}

catPic1.addEventListener('click', increment1, false);
catPic2.addEventListener('click', increment2, false);
