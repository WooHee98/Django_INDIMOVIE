

var $_GET = {};

document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
    function decode(s) {
        return decodeURIComponent(s.split("+").join(" "));
    }

    $_GET[decode(arguments[1])] = decode(arguments[2]);
});

var max = $_GET["number"]*1;
var current = 0;



	var path = window.location.pathname;
	

	var params = '';
	params += '&mt_id=' + path.split("/")[5];

	$.ajax({
		url: '/movie/getSeats',
		type: 'GET',
		data: params,
		dataType: 'json',
		contentType: false,
		processData: false,
		success: function(pResult) {
				console.log(pResult);
				$("button").each( function(pIndex){
					//console.log($(this));
					console.log(pIndex, $(this).text());
					$(this).data("id", pResult[pIndex].s_name);
					if(pResult[pIndex].s_reserved == "1"){
						$(this).attr("disabled", true);
					}
				});
				$(document).on("click", "button", function(){
					// $(this).data("id")  : android 로 보낸다. 
					if($(this).hasClass("selected")){
						$(this).removeClass("selected");
						current--;
					}
					else{
						if(current < max){
							$(this).addClass("selected");
							current++;
						}
						else{
							alert("최대 인원 초과");
						}
					}
					
				});
				$(document).on("click", "#submit", function(){
					if(current < max){
							alert("버튼을 눌러주세요");
						}
					else{

						var result = "";
						$(".selected").each(function(pIndex){
						result += "&seat"+pIndex+"="+$(this).data("id");
						});
						//result += "&num="+max;
						console.log(result);
						window.indi.testFunction(result);
						//result 를 리턴;
					}
				});
			}
		});