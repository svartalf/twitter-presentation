'use strict';

var Stream = Spine.Controller.sub({

    init: function(url) {
        this.socket = new SockJS(url);
        this.socket.onmessage = this.proxy(this.message);
    },

    message: function(response) {
        console.log(response);
    }

});