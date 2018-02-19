define(['wq/app', 'wq/map', 'wq/patterns', 'wq/photos',
        './config',
        'leaflet.draw', 'leaflet.markercluster'],
function(app, map, patterns, photos, config) {

/* import config from app/js/nvc/config
 config has attribute

 config.router = {
    'base_url': ''
};
can this be changed to change slug to
 'slug': '([^/?#]+)',
*/
app.use(map);
app.use(patterns);
app.use(photos);

config.presync = presync;
config.postsync = postsync;
var ready = app.init(config).then(function() {
    app.jqmInit();
    app.prefetchAll();
});

// Sync UI
function presync() {
    $('button.sync').html("Syncing...");
    $('li a.ui-icon-minus, li a.ui-icon-alert')
       .removeClass('ui-icon-minus')
       .removeClass('ui-icon-alert')
       .addClass('ui-icon-refresh');
}

function postsync(items) {
    $('button.sync').html("Sync Now");
    app.syncRefresh(items);
}

return ready;

});
