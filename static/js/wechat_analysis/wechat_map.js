var map_data = [];
for (var key in position_count) {
    map_data.push({
        name: key,
        value: position_count[key]
    })
}


var dom = document.getElementById("world_map");
var myChart = echarts.init(dom);




var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            });
        }
    }
    return res;
};

function renderItem(params, api) {

    var points = [];
    var color = api.visual('color');


}

var map_option = {
    // backgroundColor: '#404a59',
    title: {
        text: '微信好友地区分布',
        subtext: 'alexander提供技术支持',
        left: 'center',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip : {
        trigger: 'item',
        formatter: function(params) {
            var res;
            var myseries = map_option.series;
            for (var i = 0; i < myseries.length; i++) {
                for(var j=0;j<myseries[i].data.length;j++){

                    if(myseries[i].data[j].name===params.name){
                        res = params.name+'<br/>';
                        res+=myseries[i].name +' : '+myseries[i].data[j].value[2]+'</br>';
                        res+='经度:'+myseries[i].data[j].value[0]+'</br>';
                        res+='纬度:'+myseries[i].data[j].value[1];
                    }
                }
            }

            return res;
        }
    },
    bmap: {
        //center: [104.114129, 37.550339],
        center: [0,0],
        zoom: 1,
        roam: true,
        mapStyle: {
            styleJson: [
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": {
                        "color": "#12212d"
                    }
                },
                {
                    "featureType": "land",
                    "elementType": "all",
                    "stylers": {
                        "color": "#080719"
                    }
                },
                {
                    "featureType": "boundary",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#0a5b61"
                    }
                },
                {
                    "featureType": "railway",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#004981"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#00508b"
                    }
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "green",
                    "elementType": "all",
                    "stylers": {
                        "color": "#056197",
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "subway",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "manmade",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "local",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "boundary",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#029fd4"
                    }
                },
                {
                    "featureType": "building",
                    "elementType": "all",
                    "stylers": {
                        "color": "#2aaaff"
                    }
                },
                {
                    'featureType': 'all',     //调整所有的标签的边缘颜色
                    'elementType': 'labels.text.stroke',
                    'stylers': {
                              'color': '#313131'
                    }
          },
                {
                    'featureType': 'all',     //调整所有标签的填充颜色
                    'elementType': 'labels.text.fill',
                    'stylers': {
                              'color': '#FFFFFF'
                    }
          },

                {
                    "featureType": "label",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                }
            ]
        }
    },
    series : [

        {
            name: '好友人数',
            type: 'scatter',
            coordinateSystem: 'bmap',
            data: convertData(map_data),
            symbolSize: function (val) {
                return val[2];
            },
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#b6f410'
                }
            }
        },
        {
            name: '最多好友人数',
            type: 'effectScatter',
            coordinateSystem: 'bmap',
            data: convertData(map_data.sort(function (a, b) {
                return b.value - a.value;
            }).slice(0, 1)),
            symbolSize: function (val) {
                return val[2];
            },
            showEffectOn: 'emphasis',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
                normal: {
                    position: 'bottom',
                    show: false
                }
            },
            itemStyle: {
                normal: {

                    color: '#f49a17',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        },
        // {
        //
        //     type: 'custom',
        //     coordinateSystem: 'bmap',
        //     renderItem: renderItem,
        //     itemStyle: {
        //         normal: {
        //             opacity: 0.5
        //         }
        //     },
        //     animation: true,
        //     silent: true,
        //     data: [0],
        //     z: -10
        // }
    ]
};
if (map_option && typeof map_option === "object") {
    myChart.setOption(map_option, true);
     // 添加百度地图插件
                var bmap =myChart.getModel().getComponent('bmap').getBMap();
                bmap.addControl(new BMap.MapTypeControl());

}
