function getkeynum(){
    $.ajax({
        url:"/keynum",
        success: function (data) {
            $(".key21").text(data.confirmed)
            $(".key22").text(data.died)
            $(".key23").text(data.cured)
            $(".key24").text(data.curConfirm)
            $(".key25").text(data.overseasInput)
            $(".key31").text(data.confirmedRelative)
            $(".key32").text(data.diedRelative)
            $(".key33").text(data.curedRelative)
            $(".key34").text(data.curConfirmRelative)
            $(".key35").text(data.overseasInputRelative)
        },
        error:function(xhr,type,errorThrown){

        }

    });
}
setInterval(getkeynum,1000)