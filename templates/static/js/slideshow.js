$(function(){
    $('.national_hot').liMarquee({
        direction: 'up',
        scrollamount: 24,
    });

    $('.local_hot').liMarquee({
        direction: 'up',
        scrollamount: 12,
    });
});


window.addEventListener("resize", () => { if(map_chart != null){
            map_chart.resize();
        }
        if(geo_chart != null){
            geo_chart.resize();
        }});