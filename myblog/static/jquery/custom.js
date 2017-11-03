$(document).ready(function(){
	$("button").click(function(){
		$(".myform").filter("#"+this.id).toggle();
	});
	$("button").click(function(){
		var id = $(this).attr("id");
		if($(this).attr("class") == "btn btn-primary mybutton"){
			$(this).attr("class","btn btn-default mybutton");
		}else{
			$(this).attr("class","btn btn-primary mybutton");
		}
		$(this).load('home/post/'+id);
	});
	
});

function weather(){
	$.getJSON("https://api.weatherbit.io/v2.0/current?postal_code=560029&country=IN&key=9c54529968c94bf29156840f7d50c72a",function(result){
		$.each(result,function(key,val){
			$.each(val,function(k,v){
				$.each(v,function(kr,vr){
					if(kr=="temp"){
						$("#2").html(vr+"'Celcius");
					}else if(kr=="app_temp"){
						$("#3").html(vr+"'Celcius");
					}else if(kr=="clouds"){
						$("#4").html(vr+"%");
					}else if(kr=="wind_spd"){
						$("#5").html(vr+"KM/Hr");
					}else if(kr=="city_name"){
						$("#1").html(vr);
					}
				
			});
		});

	});
});