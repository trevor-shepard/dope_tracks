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
            $.get('/user/top_tracks/' + id + '?days=' + self.days)
            .done(function(tracks){
                self.tracks = tracks
            })

        },
        checkSubmit: function(event){
            if (event.code === 'Enter'){
                this.getTopTracks()
            }
        }
    },
    created: function(){
        this.getTopTracks()
    }
})