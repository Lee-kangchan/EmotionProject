//GPS불러오기
let ips;
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
}


//PC 모바일 확인
function mobilePcCheck(){
    var filter = "win16|win32|win64|mac|macintel";
    if (filter.indexOf(navigator.platform.toLowerCase()) < 0) {
        return navigator.userAgent;

    }else {
         return navigator.userAgent;
    }

}
//ip check
function ipcheck(){
	 // HTML의 <script> 요소를 생성한다
  const se = document.createElement('script');
  // <script> 요소의 src 속성을 설정한다
  se.src = 'https://ipinfo.io?callback=callback';
  // <body> 요소의 하위 끝에 붙인다
  // 그리고 콜백 함수를 호출한다
  document.body.appendChild(se);

  // 앞서 생성한 <script> 요소를 제거한다
}
function callback(data){
    $.ajax({
            type : 'GET',
            url : 'v1/ip?ip=' + data.ip,
            dataType: 'json',
            success : function(result){
            },
            error : function(xtr,status,error){
            }
        });

    ips = data.ip;
}
$("#gps").click(function(){

	var fd=new FormData();
    gps = getLocation();
    device = mobilePcCheck();
    fd.append("gps",gps);
    fd.append("device",device);

    $.ajax({
            type : 'POST',
            url : '/gps',
            data : fd,
            dataType: 'json',
            processData: false,    // 반드시 작성
            contentType: false,    // 반드시 작성
            success : function(result){
                if(result.data.faceYN === 'yes'){
                    alert("인증 성공")
                } else {
                    alert("인증 실패")
                }
            },
            error : function(xtr,status,error){
               alert("측정 간에 문제가 발생했습니다. 다시 시도해주세요.")
            }
        });

})
$("#logout").click(function (){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href = "/signOut?gps="+gps+"&device="+device;
})
$("#admin").click(function (){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href = "/admin?gps="+gps+"&device="+device;
})
$("#main").click(function (){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href = "/main?gps="+gps+"&device="+device;
})

$("#userlog").click(function (){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href = "/userlog?gps="+gps+"&device="+device;
})
$("#dashBoard").click(function(){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href = "/dashBoard?gps="+gps+"&device="+device;
})

function start(){
    $('#modal').modal("show");
}
function emotion(){
    gps = getLocation();
    device = mobilePcCheck();

    alert(gps+ " --" +device);
    location.href ="/emotion?gps="+gps+"&device="+device;
}