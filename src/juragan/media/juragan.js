
var INDONESIA = new google.maps.LatLng(-0.7892750, 113.9213270);

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
            zoom: 4,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: INDONESIA
        });
    },

    show: function(pos, dekat) {
        this.pos = pos;
        this._updatePosition();
        this._placePosition();
        this._loadToko();

        if (dekat != undefined) {
            this._setBounds(pos, dekat);
        }
    },

    _setBounds: function(a, b) {
        var alat = a.lat();
        var alng = a.lng();
        var blat = b.lat();
        var blng = b.lng();

        var w = Math.abs(blng - alng);
        var h = Math.abs(blat - alat);
        var w5 = w/5.0;
        var h5 = h/5.0;
        
        var south = alat < blat ? alat : blat;
        var north = alat > blat ? alat : blat;
        var west = alng < blng ? alng : blng;
        var east = alng > blng ? alng : blng;

        east -= w5;
        west += w5;
        south -= h5;
        north += h5;

        var sw = new google.maps.LatLng(south, west);
        var ne = new google.maps.LatLng(north, east);

        var bounds = new google.maps.LatLngBounds(sw, ne);
        this.map.fitBounds(bounds);
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
        $.getJSON('/toko/posisi/', function(json) {
            self._setToko(json.posisi);
        });
    },

    _setToko: function(toko) {
        for (var i=0; i<toko.length; i++) {
            var t = toko[i];
            t._pos = new google.maps.LatLng(t.lat, t.lng);
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
        content += '<p class="alamat">' + toko.alamat + '<br/>' + toko.kota + '<br/>' + toko.provinsi + '</p>';
        content += '</div>';

        var info = new google.maps.InfoWindow({
            content: content
        });
        return info;
    },
};


