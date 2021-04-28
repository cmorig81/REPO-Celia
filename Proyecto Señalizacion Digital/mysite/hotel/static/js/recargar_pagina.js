$(function () {
    setInterval(
        function(){
            $("#tablaDatos").load("/templates/hotel/datosSalasHotel.html")
        }, 2000
    );
});