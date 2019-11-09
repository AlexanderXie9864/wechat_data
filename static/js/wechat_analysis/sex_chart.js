var sex_data = [];
for (var key in sex_count) {
   sex_data.push({
        name: key,
        value: sex_count[key]
    })
}

var dom = document.getElementById("sex_chart");
var myChart = echarts.init(dom);
var app = {};

var sex_option = {
    backgroundColor: '#12212d',

    title: {
        text: '性别比例',
        left: 'center',
        top: 5,
        textStyle: {
            color: '#ccc'
        }
    },

    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },


    series : [
        {
            name:'微信好友性别比例',
            type:'pie',
            radius : '55%',
            center: ['50%', '50%'],
            data:sex_data.sort(function (a, b) { return a.value - b.value; }),
            roseType: 'radius',
            label: {
                normal: {
                    textStyle: {
                        color: 'rgba(255, 255, 255, 0.3)'
                    }
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.3)'
                    },
                    smooth: 0.2,
                    length: 10,
                    length2: 20
                }
            },
            itemStyle: {
                normal: {
                    color: '#c22228',
                    shadowBlur: 200,

                }
            },

            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
                return Math.random() * 200;
            }
        }
    ]
};;
if (sex_option && typeof sex_option === "object") {
    myChart.setOption(sex_option, true);
}