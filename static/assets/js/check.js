
//GPS불러오기
function getLocation() {
  if (navigator.geolocation) { // GPS를 지원하면
    navigator.geolocation.getCurrentPosition(function(position) {
        result = position.coords.latitude + ' ' + position.coords.longitude;
      return position.coords.latitude + ' ' + position.coords.longitude
    }, function(error) {
      console.error(error);
    }, {
      enableHighAccuracy: false,
      maximumAge: 0,
      timeout: Infinity
    });
  } else {
      result = "X";
      return "X";
  }
  return result;
}


//PC 모바일 확인
function mobilePcCheck(){
    var filter = "win16|win32|win64|mac|macintel";
    if (filter.indexOf(navigator.platform.toLowerCase()) < 0) {
        return "mobile";

    }else {
         return "PC";
    }

}
$("#logout").click(function (){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href = "/signOut?gps="+gps+"&device="+device+"";
})
$("#admin").click(function (){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href = "/admin?gps="+gps+"&device="+device+"";
})
$("#main").click(function (){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href = "/main?gps="+gps+"&device="+device+"";
})
$("#userlog").click(function (){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href = "/userlog?gps="+gps+"&device="+device+"";
})
$("#dashBoard").click(function(){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href = "/dashBoard?gps="+gps+"&device="+device+"";
})

function start(){
    $('#modal').modal("show");
}
function emotion(){
    gps = getLocation();
    device = mobilePcCheck();
    alert(gps+ " --" +device);
    location.href ="/emotion?gps="+gps+"&device="+device+"";
}