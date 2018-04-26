new Vue({
    el: "#top-tracks",
    delimiters: ["[[", "]]"],
    data: {
        tracks: [],
        days: 30,
    },
    methods: {
        getTopTracks: function(){
            var id = $('#top-tracks').attr('data-id')
            var self = this
            $.get('/group/'+ id +'/common_tracks?days=' + self.days)
            .done(function(tracks){
                var calls = tracks.map(function(track) {
                    return $.get('/track/get_recent_users/' + track.id + '?group=' + id)
                })
                $.when.apply(this, calls).done(function() {
                    for(var i = 0; i < arguments.length; i++) {
                        tracks[i].users = arguments[i][0]
                    }
                    self.tracks = tracks
                })
            })
        },
        checkSubmit: function(event){
            console.log(event.code)
            if (event.code === 'Enter'){
                this.getTopTracks()
            }
        }

    },
    created: function(){
        this.getTopTracks()

    }
    

})
