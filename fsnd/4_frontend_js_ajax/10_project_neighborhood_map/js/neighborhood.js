var locations = [
    {
        title: 'Reichstag',
        latLng: [52.518611, 13.376111],
    },
    {
        title: 'Brandenburg Gate',
        latLng: [52.516272,13.377722],
    },
    {
        title: 'German Chancellery',
        latLng: [52.52,13.369444],
    },
    {
        title: 'Bellevue Palace',
        latLng: [52.5175553, 13.3527497],
    },
    {
        title: 'Victory Column',
        latLng: [52.5145076, 13.3501100],
    },
];

var Location = function(data) {
    this.title = ko.observable(data.title);
    this.latLng = ko.observable(data.latLng);
};

var leafletLoadError = function() {
    alert('test');
};

var ViewModel = function() {
    var self = this;
    this.wikiEntries = ko.observableArray([]);
    this.wikiHeader = ko.observable("");
    this.wikiError = ko.observable("");

    // Create Locations
    this.locationList = ko.observableArray([]);

    locations.forEach(function(location) {
        self.locationList.push(new Location(location));
    });

    // Create Map
    var map = L.map('map').setView([52.518611, 13.376111], 14);

    layer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoidHJpcGxlIiwiYSI6ImNqaW9nbXVpYzBiNjUza3FlaWJqbno2aXQifQ.gZIoqCkam1hIriIj3Mr-lw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets',
        errorTileUrl: 'img/error-code.jpeg'
    });

    layer.addTo(map);

    // Load Wikipedia Data
    this.setWikiData = function(title) {
        return function() {
            var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + title + '&format=json&callback=wikiCallback';
            self.wikiEntries([]);
            self.wikiHeader("Wikipedia Articles about " + title + ":");
            self.wikiError("");

            var wikiRequestTimeout = setTimeout(function() {
                self.wikiError('Failed to get wikipedia resources in time');
            }, 2000);

            $.ajax( {
                url: wikiUrl,
                dataType: 'jsonp',
                // jsonp: 'callback',
                success: function(response) {
                    var articleList = response[1];
                    for (var i = 0; i < articleList.length; i++) {
                        articleStr = articleList[i];
                        var url = 'http://en.wikipedia.org/wiki/' + articleStr;
                        self.wikiEntries.push('<li><a href="' + url + '">' + articleStr + '</a></li>');
                    }

                    clearTimeout(wikiRequestTimeout);
                }
            });
        };
    };

    // Add Markers
    this.addMarkers = function(locationArray) {
        if (self.markers) {
            self.markers.clearLayers();
        } else {
            self.markers = L.layerGroup();
        }
        locationArray.forEach(function(location) {
            var marker = L.marker(location.latLng()).bindPopup(location.title());
            marker.on('click', self.setWikiData(location.title()));
            self.markers.addLayer(marker);
        });
        self.markers.addTo(map);
    };

    // Filter Functionality
    this.filterTerm = ko.observable("");

    this.filteredLocationList = ko.computed(function() {
        var filter = self.filterTerm().toLowerCase();
        if (!filter || filter === "") {
            self.addMarkers(self.locationList());
            return self.locationList();
        } else {
            var filteredLocations = ko.utils.arrayFilter(self.locationList(), function(location) {
                return location.title().toLowerCase().indexOf(filter) != -1;
            });
            self.addMarkers(filteredLocations);
            return filteredLocations;
        }
    });

    this.addMarkers(self.filteredLocationList());

    // Toogle Sidebar Functionality
    this.visibilityToggle = ko.observable(false);

    this.sidebarVisible = ko.pureComputed(function() {
        return self.visibilityToggle() ? "sidebarToggled" : "";
    }, ViewModel);

    this.shrinkMap = ko.pureComputed(function() {
        return self.visibilityToggle() ? "moveForSidebar" : "";
    }, ViewModel);

    this.toggleSidebar = function() {
        self.visibilityToggle(!self.visibilityToggle());
        map.invalidateSize();
    };

    // Highlight Marker
    // With leaflet it is not possible to manipulate the marker itself. The options
    // I found were removing and replacing it with a custom marker (allows different
    // images to be used) or highlighting it via another shape (which I am doing below).
    this.highlightMarker = function(data) {
        return function() {
            if (self.circle) {
                self.circle.remove();
            }
            self.circle = L.circle(data.latLng(), {
                color: 'red',
                radius: 100
            });
            self.circle.addTo(map);
        };
    };

};

ko.applyBindings(new ViewModel());
