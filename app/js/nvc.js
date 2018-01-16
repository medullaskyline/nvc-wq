requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'nvc': '../nvc',
        'data': '../data/'
    }
});

requirejs(['nvc/main']);
