function getBaseUrl() {
    var baseurl = window.location.pathname.replace("index.html",'');
    baseurl = baseurl.replace(/\/$/,'');
    if (baseurl == 'www') {
        // Windows
        baseurl = '/www';
    }
    return baseurl;
}

require.config({
    'config': {
        'nvc/config': {
             'router': {
                 'base_url': getBaseUrl()
             },
             'store': {
                 'service': 'https://medullaskyline.com',
                 'defaults': {'format': 'json'}
             },
        }
    }
});

document.addEventListener('deviceready', function() {
    require(['js/nvc'], function() {
        require(['nvc/main', 'wq/app'], function(ready, app) {
            ready.then(function() {
                app.replaceState('');
                setTimeout(navigator.splashscreen.hide, 10);
            });
        });
    });
});
