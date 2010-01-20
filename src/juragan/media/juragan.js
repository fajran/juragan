
var juragan = {
    canvas: undefined,
    pos: undefined,

    pos_marker: undefined,
    toko_path: undefined,

    infowindow: undefined,
    toko: {},

    init: function(canvas) {
        this.canvas = canvas;
        this.map = new google.maps.Map(canvas.get(0), {
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
    },

    show: function(pos) {
        this.pos = pos;
        this._updatePosition();
        this._placePosition();
        this._loadToko();
    },

    _updatePosition: function() {
        var pos = this.pos;
        this.map.setOptions({
            center: pos,
        });
    },

    _placePosition: function() {
        var pos = this.pos;
        var map = this.map;
        this.pos_marker = new google.maps.Marker({
            position: pos,
            map: map,
        });
    },

    _loadToko: function() {
        var self = this;
        $.getJSON('/toko/daftar/?format=json', function(json) {
            self._setToko(json.toko);
        });
    },

    _setToko: function(toko) {
        for (var i=0; i<toko.length; i++) {
            var t = toko[i];
            t._pos = new google.maps.LatLng(t.y, t.x);
            this.toko[t.id] = t;
            this._placeToko(t);
        }
    },

    _placeToko: function(toko) {
        if (this.toko_icon == undefined) {
            this.toko_icon = new google.maps.MarkerImage(
                                    '/+media/icons/music.png',
                                    new google.maps.Size(32, 37),
                                    new google.maps.Point(0, 0),
                                    new google.maps.Point(16, 35));
        }
        var self = this;

        toko._marker = new google.maps.Marker({
            position: toko._pos,
            map: this.map,
            icon: this.toko_icon,
        });

        google.maps.event.addListener(toko._marker, 'click', function() {
            self._showTokoInfo(toko);
        });
    },

    showToko: function(id) {
        var pos = this.toko[id]._pos;
        this.map.panTo(pos);
        this.showTokoInfo(id);
    },

    showTokoInfo: function(id) {
        this._showTokoInfo(this.toko[id]);
    },
    _showTokoInfo: function(toko) {
        if (this.infowindow != undefined) {
            this.infowindow.close();
        }
        if (toko._info == undefined) {
            toko._info = this._createTokoInfo(toko);
        }
        toko._info.open(this.map, toko._marker);
        this.infowindow = toko._info;
    },

    _createTokoInfo: function(toko) {
        var content = "";
        content += '<div id="toko-info">';
        content += '<h1><a href="/toko/'+toko.id+'/">' + toko.nama + '</a></h1>';
        if (toko.website != undefined && toko.website != null) {
            content += '<p class="web"><a target="_blank" href="' + toko.website + '">' + toko.website + '</a></p>';
        }
        content += '<p class="email">Email: <a href="mailto:' + toko.email + '">' + toko.email + '</a></p>';
        content += '<p class="alamat">' + toko.alamat + '<br/>' + toko.kota + '<br/>' + toko.provinsi + '</p>';
        content += '</div>';

        var info = new google.maps.InfoWindow({
            content: content
        });
        return info;
    },
};


