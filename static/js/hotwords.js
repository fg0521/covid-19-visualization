
function hotwords(){
    $.ajax({
        url:"/hotwords",
        type: "GET",
        timeout:10000,
        success: function (data) {
            $(".china1").text(data.word1[0]);
            $(".china1").attr("href",data.word1[1]);
            $(".china2").text(data.word2[0]);
            $(".china2").attr("href",data.word2[1]);
            $(".china3").text(data.word3[0]);
            $(".china3").attr("href",data.word3[1]);
            $(".china4").text(data.word4[0]);
            $(".china4").attr("href",data.word4[1]);
            $(".china5").text(data.word5[0]);
            $(".china5").attr("href",data.word5[1]);
            $(".china6").text(data.word6[0]);
            $(".china6").attr("href",data.word6[1]);
            $(".china7").text(data.word7[0]);
            $(".china7").attr("href",data.word7[1]);
            $(".china8").text(data.word8[0]);
            $(".china8").attr("href",data.word8[1]);
            $(".china9").text(data.word9[0]);
            $(".china9").attr("href",data.word9[1]);
            $(".china10").text(data.word10[0]);
            $(".china10").attr("href",data.word10[1]);
            $(".china11").text(data.word11[0]);
            $(".china11").attr("href",data.word11[1]);
            $(".china12").text(data.word12[0]);
            $(".china12").attr("href",data.word12[1]);
            $(".china13").text(data.word13[0]);
            $(".china13").attr("href",data.word13[1]);
            $(".china14").text(data.word14[0]);
            $(".china14").attr("href",data.word14[1]);
            $(".china15").text(data.word15[0]);
            $(".china15").attr("href",data.word15[1]);
            $(".china16").text(data.word16[0]);
            $(".china16").attr("href",data.word16[1]);
            $(".china17").text(data.word17[0]);
            $(".china17").attr("href",data.word17[1]);
            $(".china18").text(data.word18[0]);
            $(".china18").attr("href",data.word18[1]);
            $(".china19").text(data.word19[0]);
            $(".china19").attr("href",data.word19[1]);
            $(".china20").text(data.word20[0]);
            $(".china20").attr("href",data.word20[1]);
        },
        error:function(xhr,type,errorThrown){

        }

    });
}
setInterval(hotwords,1000)

