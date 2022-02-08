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
            window.addEventListener("resize", () => { map_chart.resize();});
            }
        });
    }