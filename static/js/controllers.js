'use strict';

var Stream = Spine.Controller.sub({

    el: $('body'),

    elements: {
        '#tweets-stream': 'stream',
        '#pause-overlay': 'overlay',
        '#pause-overlay h3': 'counter'
    },

    events: {
        'keypress': 'pause'
    },

    _url: null,

    // el: $('#tweets-stream'),

    queue: [],

    interval_id: null,

    init: function(url) {
        this._url = url;

        Tweet.bind('create', this.proxy(this.create));
        this.interval_id = window.setInterval(this.proxy(this.show), 5000);

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
        this.queue.unshift(object);
        this.__update_counter();
    },

    show: function() {
        var object = this.queue.pop();
        if (!object)
            return;

        this.__update_counter();

        return this.stream.prepend(ich.tweet({
            id: object.id,
            user: object.user().name,
            profile_image_url: object.user().image(),
            text: object.html()
        }));
    },

    pause: function() {
        if (this.interval_id) {
            window.clearInterval(this.interval_id);
            this.interval_id = null;
            this.overlay.show();
        } else {
            this.interval_id = window.setInterval(this.proxy(this.show), 5000);
            this.overlay.hide();
            this.show();
        }
    },

    __update_counter: function() {
        this.counter.html('+'+this.queue.length+' '+this.__pluralize(this.queue.length, 'твит', 'твита', 'твитов'));
    },

    __pluralize: function(value, str1, str2, str3) {
        function plural(a) {
            if ( a % 10 == 1 && a % 100 != 11 )
                return 0;
            else if ( a % 10 >= 2 && a % 10 <= 4 && ( a % 100 < 10 || a % 100 >= 20))
                return 1;
            else
                return 2;
        }

        switch (plural(value)) {
            case 0:
                return str1;
            case 1:
                return str2;
            default:
                return str3;
        }
    }

});
