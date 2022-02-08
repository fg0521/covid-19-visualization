
    function btnClick() {
        var isChecked = document.getElementById("aswitch");
    
        var map_chart = echarts.getInstanceByDom(document.getElementById("map1"));
        var geo_chart = echarts.getInstanceByDom(document.getElementById("map1"));
    
        if (!isChecked.checked){
            if(geo_chart != null){
                geo_chart.clear();
                geo_chart.dispose();
            }
            
                var map_chart = echarts.init(document.getElementById("map1"), 'white', {renderer: 'canvas'});
                $(function () {
                    mapData(map_chart);
                    setInterval(mapData, 60000);
                    }
                );
                function mapData() {
                    $.ajax({
                        type: "GET",
                        url: "/mapChart",
                        dataType: 'json',
                        success: function (result) {
                            map_chart.setOption(result,true);  
                            // window.addEventListener("resize", function () {
                            //     map_chart.resize();
                            // });
                            window.addEventListener("resize", () => { 
                                map_chart.resize();
                            });
                        }
                    });
                }
            
            
        }
        else{
            if(map_chart != null){
                geo_chart.clear();
                map_chart.dispose();
            }
                var geo_chart = echarts.init(document.getElementById("map1"), 'white', {renderer: 'canvas'});
                $(function () {
                    geoData(geo_chart);
                    setInterval(geoData, 60000);
                    }
                );
                function geoData() {
                    $.ajax({
                        type: "GET",
                        url: "/geoChart",
                        // dataType: 'json',
                        success: function (result) {
                            var re_obj = (new Function("return " + result))();
                            geo_chart.setOption(re_obj,true);  
                            // window.addEventListener("resize", function () {
                            //     geo_chart.resize();
                            // });
                            window.addEventListener("resize", () => { geo_chart.resize();});
                        }
                    });
                }
            }
        
        
        
    }