'use strict';

var Stream = Spine.Controller.sub({

    _url: null,

    el: $('#tweets-stream'),

    queue: [],

    init: function(url) {
        this._url = url;

        Tweet.bind('create', this.proxy(this.create));
        window.setInterval(this.proxy(this.show), 5000);

        this._connect();
    },

    _connect: function() {
        this.socket = new SockJS(this._url);
        this.socket.onmessage = this.proxy(this.message);
        this.socket.onclose = function() {
            window.setTimeout(this._connect(), 5000);
        }
    },

    message: function(response) {
        var cls = window[response.data.class];
        switch (response.data.action) {
            case 'create':
                cls.create(response.data.data);
                break;
        }
    },

    create: function(object, event) {
        this.queue.push(object);
    },

    show: function() {
        var object = this.queue.shift();
        if (!object)
            return;

        return this.el.prepend(ich.tweet({
            id: object.id,
            user: object.user().name,
            profile_image_url: object.user().image(),
            text: object.html()
        }));
    }

});
