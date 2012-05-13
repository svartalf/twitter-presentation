'use strict';

var Stream = Spine.Controller.sub({

    el: $('#tweets-stream'),

    queue: [],

    init: function(url) {
        this.socket = new SockJS(url);
        this.socket.onmessage = this.proxy(this.message);

        Tweet.bind('create', this.proxy(this.create));
        window.setInterval(this.proxy(this.show), 5000);
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
