'use strict';

var Stream = Spine.Controller.sub({

    el: $('#tweets-stream'),

    queue: [],

    init: function(url) {
        this.socket = new SockJS(url);
        this.socket.onmessage = this.proxy(this.message);

        Tweet.bind('create', this.proxy(this.create));
        window.setInterval(this.proxy(this.show), 1000);
    },

    message: function(response) {
        var cls = window[response.data.class];
        var data = response.data.data;
        switch (response.data.action) {
            case 'create':
                cls.create({
                    id: data.id,
                    user_id: data.user_id,
                    text: data.text,
                    created_at: new Date(data.created_at*1000)
                });
                break;
        }
    },

    create: function(object, event) {
        this.queue.push(object);
        if (!object.user()) {
            User.fetch({id: object.user_id});
        }
    },

    show: function() {
        var object = this.queue.shift();
        if (!object)
            return;
        var template = ich.tweet({
            id: object.id,
            user: object.user().name,
            profile_image_url: object.user().profile_image_url,
            text: object.html()
        });
        this.el.prepend(template);
    }

});
