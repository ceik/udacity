var catCount = 5;

var model = {
    currentCat: null,
        init: function() {
        if (!localStorage.catData) {
            var catData = [];
            for(var i = 0; i < catCount; i++) {
                var catObj = {
                    name : i,
                    img_path: 'img/cat' + i + '.jpg',
                    clickCounter: 0
                };
                console.log(catObj);
                catData.push(catObj);
            }
            localStorage.setItem('catData', JSON.stringify(catData));
        }
    },
    getAllCats: function() {
        return JSON.parse(localStorage.catData);
    }
};

var octopus = {
    init: function() {
        model.init();
        model.currentCat = model.getAllCats()[0];
        view.init();
        view.renderList();
    },
    getCurrentCat: function() {
        return model.currentCat;
    },
    setCurrentCat: function(cat) {
        model.currentCat = cat;
    },
    getCats: function() {
        return model.getAllCats();
    },
    increment: function() {
        model.currentCat.clickCounter++;
        view.renderCat();
        view.formClicks.value = model.currentCat.clickCounter;
    },
    saveData: function() {
        model.currentCat.name = view.formName.value;
        model.currentCat.img_path = view.formUrl.value;
        model.currentCat.clickCounter = view.formClicks.value;
        view.counter.textContent = model.currentCat.clickCounter;
        view.hideAdmin();
    }
};

var view = {
    init: function() {
        this.catList = document.getElementById("cat-list");
        this.catName = document.getElementById("cat-name");
        this.catPic = document.getElementById("cat-pic");
        this.counter = document.getElementById("counter");
        this.catPic.addEventListener('click', function() {
            octopus.increment();
        });
        this.adminButton = document.getElementById("admin-button");
        this.adminButton.addEventListener('click', function() {
            view.showAdmin();
        });
        this.adminArea = document.getElementById("admin-area");
        this.adminArea.style.visibility = 'hidden';
        this.adminForm = document.getElementById("admin-form");
        this.formName = document.getElementById("form-name");
        this.formUrl = document.getElementById("form-url");
        this.formClicks = document.getElementById("form-clicks");
        this.cancelButton = document.getElementById("cancel-button");
        this.cancelButton.addEventListener('click', function() {
            view.hideAdmin();
        });
        this.saveButton = document.getElementById("save-button");
        this.saveButton.addEventListener('click', function() {
            octopus.saveData();
        });
    },
    renderList: function() {
        octopus.getCats().forEach(function(cat) {
            var elem = document.createElement('li');
            elem.textContent = 'Cat '+ cat.name;
            elem.addEventListener('click', (function(catCopy) {
                return function() {
                    octopus.setCurrentCat(catCopy);
                    view.renderCat();
                };
            }) (cat));
            view.catList.appendChild(elem);
        });
    },
    renderCat: function() {
        var currentCat = octopus.getCurrentCat();
        this.catName.textContent = 'Cat ' + currentCat.name;
        this.catPic.innerHTML = '<img src="' + currentCat.img_path + '">';
        this.counter.textContent = currentCat.clickCounter;
    },
    hideAdmin: function() {
        this.adminArea.style.visibility = 'hidden';
    },
    showAdmin: function() {
        var currentCat = octopus.getCurrentCat();
        this.formName.value = '';
        this.formUrl.value = '';
        this.formClicks.value = '';
        this.adminArea.style.visibility = 'visible';
        this.formName.value = currentCat.name;
        this.formUrl.value = currentCat.img_path;
        this.formClicks.value = currentCat.clickCounter;
    }
};

octopus.init();
