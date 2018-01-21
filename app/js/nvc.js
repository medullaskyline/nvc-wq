requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'nvc': '../nvc',
        'data': '../data/'
    }
});

requirejs(['nvc/main']);

define(['wq/model'], function(model) {
//   var items = model('/items');
//   var types = model({'url': 'types'});

/*
https://wq.io/1.0/docs/model-js
query	The wq/store.js query to use when retrieving data for the model. This is often an object of the form {'url': url}.
functions	A collection of computable attributes that can be applied to items in the model
store	The wq/store.js instance to use for the model. This defaults to the main instance (ds) if not set.
url	A shortcut for setting {'query': {'url': url}}.
max_local_pages	The maximum number of paginated server responses to store locally. This should almost always be 1 (the default). Most operations requiring fast and/or offline capabilities will be completed with the first page of data. Subsequent pages (if any) will be loaded on-demand via ds.fetch()
partial	Flag indicating that not all data is stored locally. This should be set whenever you expect there to be more than max_local_pages worth of data in the server database.
reversed	Set to true if the data is sorted in reverse chronological order. If set, new items (added via update()) will be placed at the beginning of the list instead of the end.

// Filter on existing field
myModel.filter({'type_id': 3}).then(function(type3items) {
    type3items.forEach(function(item) {
        console.log(item.id, item.label);
    });
});

// Filter on a computed field
var functions = {
    'big': function(item) {
        return item.size > 100;
    }
};
var myModel = model({'url': items', 'functions': functions});
myModel.filter({'big': true}).then(function(bigItems) {
    bigItems.forEach(function(item) {
        console.log(item.id, item.label);
    });
});

*/
});