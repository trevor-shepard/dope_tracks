new Vue({
    el: "#top-tracks",
    delimiters: ["[[", "]]"],
    data: {
        tracks: [],
        days: 30,
        loading:false,
    },
    methods: {
        getTopTracks: function(){
            this.loasing=true;
            var id = $('#top-tracks').attr('data-id')
            var self = this
            $.get('/user/top_tracks/' + id + '?days=' + self.days)
            .done(function(tracks){
                self.tracks = tracks
                self.loading = false;
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

new Vue({
    el: "#top-tags",
    delimiters: ["[[", "]]"],
    data: {
        tags: [],
        days: 30,
        loading:false,
    },
    methods: {
        getTopTags: function(){
            this.loading=true;
            var id = $('#top-tracks').attr('data-id')
            var self = this;
            $.get('/user/top_tags/' + id + '?days=' + self.days)
            .done(function(tags){
                self.tags = tags
                self.loading = false;
            });
        },
        checkSubmit: function(event){
            if (event.code === 'Enter'){
                this.getTopTracks()
            }
        }
    },
    created: function(){
        this.getTopTags()
    }
})

