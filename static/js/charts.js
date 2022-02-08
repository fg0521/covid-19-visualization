var line_chart = echarts.init(document.getElementById("tend_chart"), 'white', {renderer: 'canvas'});
var liquid_chart = echarts.init(document.getElementById("percent_chart"), 'white', {renderer: 'canvas'});
var bar_chart = echarts.init(document.getElementById("infect_chart"), 'white', {renderer: 'canvas'});
var line2_chart = echarts.init(document.getElementById("input_chart"), 'white', {renderer: 'canvas'});
var map2_chart = echarts.init(document.getElementById("map2"), 'white', {renderer: 'canvas'});
var wordcloud_chart = echarts.init(document.getElementById("wc_chart"), 'white', {renderer: 'canvas'});
var bmap_chart = echarts.init(document.getElementById("bdmap"), 'white', {renderer: 'svg'});


$(
    function () {
        bmapData(bmap_chart);
        setInterval(bmapData, 60000);
    }
);
function bmapData() {

    // $.ajax里不要指定dataType: 'json'， 因为我们要的就是上面后端传过来的原始的含有str:function的字串。（这里如果指定了dataType: 'json'， 会因为转换json失败根本就进不了success: function）
    // 在success: function里把这个字串直接转为object：
    // var re_obj = (new Function("return " + result))();
    // 然后就可以chart.setOption(re_obj);
    $.ajax({
        type: "GET",
        url: "/bmapChart",
        // dataType: 'json',
        success: function (result) {
            var re_obj = (new Function("return " + result))();
            bmap_chart.setOption(re_obj);
            // window.addEventListener("resize", function () {
            //     console.log('111')
            //     bmap_chart.resize();
            // });
            // window.addEventListener("resize", () => { 
            //     console.log('111')
            //     bmap_chart.resize();
            // });
            var bmap = bmap_chart.getModel().getComponent('bmap').getBMap();
            
            var copyright = new BMap.CopyrightControl({anchor: 2, offset: {width: 2, height: 2}});
            copyright.addCopyright({id: 1, content: "\u7248\u6743\u7684\u552f\u4e00\u6807\u8bc6,\u7248\u6743\u5185\u5bb9,\u5176\u9002\u7528\u7684\u533a\u57df\u8303\u56f4\u3002"});
            bmap.addControl(copyright);
            geolocationControl = new BMap.GeolocationControl({anchor: 1, offset: {width: 10, height: 10}, showAddressBar: true, enableAutoLocation: true})
            bmap.addControl(geolocationControl)

            geolocationControl.addEventListener("locationSuccess", function(e){
                // 定位成功事件
                var address = '';
                address += e.addressComponent.province;
                address += e.addressComponent.city;
                address += e.addressComponent.district;
                address += e.addressComponent.street;
                address += e.addressComponent.streetNumber;
                document.getElementById('my_pos').innerHTML = '您的位置是:' + address;
                // alert("当前定位地址为：" + address);
              });
              geolocationControl.addEventListener("locationError",function(e){
                // 定位失败事件
                document.getElementById('my_pos').innerHTML = e.message;
              });
        },
    });
}

    

$(
    function () {
        lineData(line_chart);
        setInterval(lineData, 60000);
    }
);
function lineData() {
    $.ajax({
        type: "GET",
        url: "/lineChart",
        dataType: 'json',
        success: function (result) {
            line_chart.setOption(result)
            // window.addEventListener("resize", function () {
            //     line_chart.resize();
            // });  
            // window.addEventListener("resize", () => { line_chart.resize();});
        }
    });
}


$(
    function () {
        liquidData(liquid_chart);
        setInterval(liquidData, 60000);
    }
);
function liquidData() {
    $.ajax({
        type: "GET",
        url: "/liquidChart",
        dataType: 'json',
        success: function (result) {
            liquid_chart.setOption(result) 
            // window.addEventListener("resize", function () {
            //     liquid_chart.resize();
            // }); 
            // window.addEventListener("resize", () => { liquid_chart.resize();});
        }
    });
}


$(
    function () {
        barData(bar_chart);
        setInterval(barData, 60000);
    }
);
function barData() {
    $.ajax({
        type: "GET",
        url: "/barChart",
        dataType: 'json',
        success: function (result) {
            bar_chart.setOption(result)
            // window.addEventListener("resize", function () {
            //     bar_chart.resize();
            // });
            // window.addEventListener("resize", () => { bar_chart.resize();});

        }
    });
}
    

$(
    function () {
        line2Data(line2_chart);
        setInterval(line2Data, 60000);
    }
);
function line2Data() {
    $.ajax({
        type: "GET",
        url: "/line2Chart",
        dataType: 'json',
        success: function (result) {
            line2_chart.setOption(result)  
            // window.addEventListener("resize", function () {
            //     line2_chart.resize();
            // });
            // window.addEventListener("resize", () => { line2_chart.resize();});
        }
    });
}




    
$(
    function () {
        map2Data(map2_chart);
        setInterval(map2Data, 60000);
    }
);
function map2Data() {
    $.ajax({
        type: "GET",
        url: "/map2Chart",
        dataType: 'json',
        success: function (result) {
            map2_chart.setOption(result)  
            // window.addEventListener("resize", function () {
            //     map2_chart.resize();
            // });
            // window.addEventListener("resize", () => { map2_chart.resize();});
        }
    });
}

$(
    function () {
        wordcloudData(wordcloud_chart);
        setInterval(wordcloudData, 60000);
    }
);

function wordcloudData() {
    $.ajax({
        type: "GET",
        url: "/wordcloudChart",
        dataType: 'json',
        success: function (result) {
            wordcloud_chart.setOption(result)  
            // window.addEventListener("resize", function () {
            //     wordcloud_chart.resize();
            // });
            // window.addEventListener("resize", () => { wordcloud_chart.resize();});
        }
    });
}




window.addEventListener("resize", () => { 
    this.bar_chart.resize();
    this.line_chart.resize();
    this.line2_chart.resize();
    this.liquid_chart.resize();
    this.bmap_chart.resize();
    this.map2_chart.resize();
    this.wordcloud_chart.resize();
    
});
// $(window).resize(function() {
//     setTimeout(function(){
//             bar_chart.resize();
//         line_chart.resize();
//         line2_chart.resize();
//         liquid_chart.resize();
//         bmap_chart.resize();
//         map2_chart.resize();
//         wordcloud_chart.resize();
//         // geo_chart.resize();
//     },100)
// });




