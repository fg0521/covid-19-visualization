function gettime(){
    $.ajax({
        url:"/time",
        type: "GET",
        timeout:10000,
        success: function (data) {
            $(".time").html(data);
        },
        error:function(xhr,type,errorThrown){
        }
    });
}
setInterval(gettime,1000)