
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // Load streetview Image and change greeting
    var $street = $('#street').val();
    var $city = $('#city').val();

    var address = $street + ', ' + $city
    var gmaps_url = 'http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + address
    var img_html = '<img class="bgimg" src="' + gmaps_url + '">'

    $body.append(img_html);
    $greeting.text('So you want to live at ' + $street + 'in ' + $city + '?')

    // Load NYT Data
    var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    url += '?' + $.param({
      'api-key': "XXX",
      'q': address,
      'sort': "newest",
      'fl': "headline, snippet, web_url"
    });

    // Own solution
    // $.getJSON(url, function(data) {
    //     var items = []
    //     $.each(data.response.docs, function(key, value) {
    //         items.push('<li class="article"><a href="' + value.web_url + '">' + value.headline.main + '</a><p>"' + value.snippet + '</p></li>');
    //     });

    //     $(".article-list").append(items.join(""))
    // });

    // Course Solution
    var nytUrl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + address + '&sort=newest&api-key=XXX'

    $.getJSON(nytUrl, function(data) {
        $nytHeaderElem.text('NYT Articles about ' + address);

        articles = data.response.docs;
        for(var i = 0; i < articles.length; i++) {
            var article = articles[i];
            $nytElem.append('<li class="article"><a href="' + article.web_url + '">' + article.headline.main + '</a><p>"' + article.snippet + '</p></li>')
        }
    }).fail(function() {
        $nytHeaderElem.text('NYT Articles Could Not Be Loaded');
    })

    // Load Wikipedia Data
    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + address + '&format=json&callback=wikiCallback';

    var wikiRequestTimeout = setTimeout(function() {
        $wikiElem.text('Failed to get wikipedia resources in time');
    }, 8000);

    $.ajax( {
        url: wikiUrl,
        dataType: 'jsonp',
        // jsonp: 'callback',
        success: function(response) {
            var articleList = response[1];
            console.log(response)
            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i];
                var url = 'http://en.wikipedia.org/wiki/' + articleStr;
                $wikiElem.append('<li><a href="' + url + '">' + articleStr + '</a></li>');
            };

            clearTimeout(wikiRequestTimeout);
        }
    });


    return false;
};

$('#form-container').submit(loadData);
