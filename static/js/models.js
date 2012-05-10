'use strict';

var User = Spine.Model.sub();
User.configure('User', 'name', 'profile_image_url');
User.extend(Spine.Model.Ajax);
User.extend({
    url: '/users/'
});

var Tweet = Spine.Model.sub();
Tweet.configure('Tweet', 'user', 'text', 'created_at');
Tweet.belongsTo('user', 'User');
