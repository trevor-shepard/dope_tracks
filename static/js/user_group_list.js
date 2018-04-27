new Vue({
    el: "#group-list",
    delimiters: ["[[", "]]"],
    data: {
        groups: [],
    },
    methods: {
        getUserGroups: function(){
            var id = $('#group-list').attr('data-id')
            var self = this
            $.get('/user/get_group_list/' + id)
            .done(function(groups){
                console.log(groups)
                self.groups = groups
            })
        }
    },
    created: function(){
        this.getUserGroups()
    }

})