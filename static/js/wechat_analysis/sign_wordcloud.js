
var word_data = [];
for (var key in word_count) {
    word_data.push({
        name: key,
        value: word_count[key]
    })
}
var maskImage = new Image();
maskImage.src = '/static/img/timg.jpg';
var word_cloud_option = {
    title: {
        text: '微信好友签名词云',
        x: 'center',
        textStyle: {
            fontSize: 23,
            fontColor:'#12212d'
        }

    },
    backgroundColor: '#040404',
    series: [{
        name: '微信好友签名词云',
        type: 'wordCloud',
        //size: ['9%', '99%'],
        sizeRange: [12, 80],
        //textRotation: [0, 45, 90, -45],
        rotationRange: [-45, 90],
        //shape: 'circle',
        maskImage: maskImage,
        textPadding: 0,
        autoSize: {
            enable: true,
            minSize: 6
        },
        textStyle: {
            normal: {
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data: word_data
    }]
};
var myChart = echarts.init(document.getElementById('word_cloud'));
maskImage.onload = function() {
    if (word_cloud_option && typeof word_cloud_option === "object") {
        myChart.setOption(word_cloud_option, true);
    }
};
window.onresize = function() {
    myChart.resize();
};
