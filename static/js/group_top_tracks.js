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
                tracks.forEach(function(track, i) {
                    $.get('/track/get_recent_users/' + track.id)
                    .done(function(users) {
                        self.tracks[i].users = users
                        self.tracks = tracks
                    })
                })
                console.log(self.tracks)
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
