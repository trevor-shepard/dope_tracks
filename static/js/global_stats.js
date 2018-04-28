new Vue({
    el: "#top-tracks",
    delimiters: ["[[", "]]"],
    data: {
        topCommonTracks: [],
        topPlayedTracks:[],
        days: 30,
        trackView: true,
    },
    methods: {
        getTopCommonTracks: function(){
            var id = $('#top-tracks').attr('data-id')
            var self = this
            $.get('/global/common_plays' + '?days=' + self.days)
            .done(function(tracks){
                self.topCommonTracks = tracks
            })

        },
        getTopPlayedTracks: function(){
            var id = $('#top-tracks').attr('data-id')
            var self = this
            $.get('/global/top_plays' + '?days=' + self.days)
            .done(function(tracks){
                self.topPlayedTracks = tracks
            })

        },

        checkSubmit: function(event){
            if (event.code === 'Enter'){
                this.getTopCommonTracks()
                this.getTopPlayedTracks()
            }
        }
    },
    created: function(){
        this.getTopCommonTracks()
        this.getTopPlayedTracks()
    }
})