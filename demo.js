var resourceWait  = 30000,
    maxRenderWait = 100000,
    url           = 'http://aso100.com/rank/release/date/2016-05-03';

var page          = require('webpage').create(),
    count         = 0,
    forcedRenderTimeout,
    renderTimeout;

page.settings.javascriptEnabled = true;
page.settings.loadImages = true;
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';

page.open(url, function (status) {
    if (status !== "success") {
        console.log('Unable to load url');
        phantom.exit();
    } else {
        forcedRenderTimeout = setTimeout(function () {
            console.log(count);
            doRender();
        }, maxRenderWait);
    }
});

function doRender() {
	page.render('aso.png');
	console.log('Hello, world!');
	/*console.log('Stripped down page text:\n' + page.content);*/
  	var cookies = page.cookies;
  	
  	console.log('Listing cookies:');
  	for(var i in cookies) {
  	  console.log(cookies[i].name + '=' + cookies[i].value);
  	}
    phantom.exit();
}

page.onResourceRequested = function (req) {
    count += 1;
    console.log('> ' + req.id + ' - ' + req.url);
    clearTimeout(renderTimeout);
};

page.onResourceReceived = function (res) {
    if (!res.stage || res.stage === 'end') {
        count -= 1;
        console.log(res.id + ' ' + res.status + ' - ' + res.url);
        if (count === 0) {
            renderTimeout = setTimeout(doRender, resourceWait);
        }
    }
};

