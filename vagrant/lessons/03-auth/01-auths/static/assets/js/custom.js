var transparentDemo = true;
var fixedTop = false;

$(window).scroll(function (e) {
    oVal = ($(window).scrollTop() / 170);
    $(".blur").css("opacity", oVal);

});
$(document).ready(function () {
    $('#anchor-restaurants').click( function(){
        console.log("teste");
        $('#main-title').css('display', 'none');
        $('#restaurants').css('display', 'block');
    });
    $('#anchor-home').click( function(){
        console.log("teste");
        $('#main-title').css('display', 'block');
        $('#restaurants').css('display', 'none');
    });
});
