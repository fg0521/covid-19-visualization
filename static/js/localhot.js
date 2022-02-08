
function local_hot(){
    $.ajax({
        url:"/local_hot",
        type: "GET",
        timeout:10000,
        success: function (data) {
            $(".hz1").text(data.word1[0]);
            $(".hz1").attr("href",data.word1[1]);
            $(".hz2").text(data.word2[0]);
            $(".hz2").attr("href",data.word2[1]);
            $(".hz3").text(data.word3[0]);
            $(".hz3").attr("href",data.word3[1]);
            $(".hz4").text(data.word4[0]);
            $(".hz4").attr("href",data.word4[1]);
            $(".hz5").text(data.word5[0]);
            $(".hz5").attr("href",data.word5[1]);
            $(".hz6").text(data.word6[0]);
            $(".hz6").attr("href",data.word6[1]);
            $(".hz7").text(data.word7[0]);
            $(".hz7").attr("href",data.word7[1]);
            $(".hz8").text(data.word8[0]);
            $(".hz8").attr("href",data.word8[1]);
            $(".hz9").text(data.word9[0]);
            $(".hz9").attr("href",data.word9[1]);
            $(".hz10").text(data.word10[0]);
            $(".hz10").attr("href",data.word10[1]);
            $(".hz11").text(data.word11[0]);
            $(".hz11").attr("href",data.word11[1]);
            $(".hz12").text(data.word12[0]);
            $(".hz12").attr("href",data.word12[1]);
            $(".hz13").text(data.word13[0]);
            $(".hz13").attr("href",data.word13[1]);
            $(".hz14").text(data.word14[0]);
            $(".hz14").attr("href",data.word14[1]);
            $(".hz15").text(data.word15[0]);
            $(".hz15").attr("href",data.word15[1]);
            // $(".hz16").text(data.word16[0]);
            // $(".hz16").attr("href",data.word16[1]);
            // $(".hz17").text(data.word17[0]);
            // $(".hz17").attr("href",data.word17[1]);
            // $(".hz18").text(data.word18[0]);
            // $(".hz18").attr("href",data.word18[1]);
            // $(".hz19").text(data.word19[0]);
            // $(".hz19").attr("href",data.word19[1]);
            // $(".hz20").text(data.word20[0]);
            // $(".hz20").attr("href",data.word20[1]);
        },
        error:function(xhr,type,errorThrown){

        }

    });
}
setInterval(local_hot,1000)

