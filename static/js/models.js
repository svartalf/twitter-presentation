'use strict';

var User = Spine.Model.sub();
User.configure('User', 'name', 'profile_image_url');
User.extend(Spine.Model.Ajax);
User.extend({
    url: '/users'
});

var Tweet = Spine.Model.sub();
Tweet.configure('Tweet', 'user', 'text', 'created_at');
Tweet.belongsTo('user', 'User');
Tweet.include({
    html: function() {
        var url_re = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/gi;
        var hashtag_re = /#(\S+)/gi;
        var username_re = /@([a-z_])+/gi;

        return this.text.replace(url_re, function(match){
            return '<a href="'+match+'">'+match+'</a>';
        }).replace(hashtag_re, function(match){
            return '<a href="https://twitter.com/#!/search/'+encodeURIComponent(match.replace('#', ''))+'">'+match+'</a>';
        }).replace(username_re, function(match){
            return '<a href="https://twitter.com/#!/'+match.replace('@', '')+'">'+match+'</a>';
        });
    }
});