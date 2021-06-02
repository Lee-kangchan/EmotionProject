//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record
if (/Chrome\/(\d+\.\d+.\d+.\d+)/.test(navigator.userAgent)) {
        // Let's log a warning if the sample is not supposed to execute on this
        // version of Chrome.
        if (56 > parseInt(RegExp.$1)) {
            ChromeSamples.setStatus('Warning! Keep in mind this sample has been tested with Chrome ' + 56 + '.');
        }
    }
// var recordButton = document.getElementById("recordButton");
// var stopButton = document.getElementById("stopButton");
// var pauseButton = document.getElementById("pauseButton");

// //add events to those 2 buttons
// recordButton.addEventListener("click", startRecording);
// stopButton.addEventListener("click", stopRecording);
// pauseButton.addEventListener("click", pauseRecording);
function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia()
	*/

	// recordButton.disabled = true;
	// stopButton.disabled = false;
	// pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format
		document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/*
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	// recordButton.disabled = false;
    	// stopButton.disabled = true;
    	// pauseButton.disabled = true
	});
}

// function pauseRecording(){
// 	console.log("pauseButton clicked rec.recording=",rec.recording );
// 	if (rec.recording){
// 		//pause
// 		rec.stop();
// 		pauseButton.innerHTML="Resume";
// 	}else{
// 		//resume
// 		rec.record()
// 		pauseButton.innerHTML="Pause";
//
// 	}
// }

function stopRecording() {
	console.log("stopButton clicked");

	// //disable the stop button, enable the record too allow for new recordings
	// stopButton.disabled = true;
	// recordButton.disabled = false;
	// pauseButton.disabled = true;
	//
	// //reset button just in case the recording is stopped while paused
	// pauseButton.innerHTML="Pause";

	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {

	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//name of .wav file to use during upload and download (without extendion)
	var filename = "test";

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//upload link
	var upload = document.createElement('a');
	upload.href="#";
	upload.innerHTML = "Upload";
	var xhr=new XMLHttpRequest();
	// xhr.onload=function(e) {
	// 	if(this.readyState === 4) {
	// 		console.log("Server returned: ",e.target.responseText);
	//  	}
	// };
	var fd=new FormData();

	const canvas = document.getElementById('canvas');
    var img_url = canvas.toDataURL('image/png');
	fd.append("imgSrc", img_url);
	fd.append("audio_data", blob, filename);

    gps = getLocation();
    device = mobilePcCheck();
    fd.append("gps",gps);
    fd.append("device",device);

	$.ajax({
            type : 'POST',
            url : 'v1/emotion',
            data : fd,
            dataType: 'json',
            processData: false,    // 반드시 작성
            contentType: false,    // 반드시 작성
            success : function(result){
                if(result.data.faceYN === 'yes'){
                    window.location.href ='/emotion/result?face_negative=' + result.data.face_negative + '&face_positive=' + result.data.face_positive + '&voice_negative=' + result.data.voice_negative + '&voice_positive=' + result.data.voice_positive;
                } else {
                    window.location.href ='/re_auth';
                }
            },
            error : function(xtr,status,error){
               alert("측정 간에 문제가 발생했습니다. 다시 시도해주세요.")
            }
        });

	// xhr.open("POST","v1/emotion",true);
	// xhr.send(fd);
}

 var imageCapture;
 onGetUserMediaButtonClick()
    function onGetUserMediaButtonClick() {
        const webcamElement = document.getElementById('webcam');
                const canvasElement = document.getElementById('canvas');
                const snapSoundElement = document.getElementById('snapSound');
                const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);
                webcam.start()
                  .then(result =>{
                    console.log("webcam started");

                    console.log("webcam started");
                    setTimeout(function (){

                        let picture = webcam.snap();
                        document.querySelector('#download-photo').href = picture;
                    }, 1000)
                  })
                  .catch(err => {
                    console.log(err);
                });

                const canvas = document.querySelector('#grabFrameCanvas');
                //여기서 보내면 됩니다
                setTimeout(1000)
                let picture = webcam.snap();
                // document.querySelector('#download-photo').href = picture;
                console.log(picture);
                console.log("뭐지")
                drawCanvas(canvas,picture );
    }
    function onTakePhotoButtonClick() {
        const canvas = document.querySelector('#grabFrameCanvas');
        //여기서 보내면 됩니다
                setTimeout(1000)
        let picture = webcam.snap();
        console.log(picture);
        document.querySelector('#download-photo').href = picture;
        drawCanvas(canvas,webcam.snap() );
    }
function drawCanvas(canvas, img) {
        canvas.width = getComputedStyle(canvas).width.split('px')[0];
        canvas.height = getComputedStyle(canvas).height.split('px')[0];
        let ratio = Math.min(canvas.width / img.width, canvas.height / img.height);
        let x = (canvas.width - img.width * ratio) / 2;
        let y = (canvas.height - img.height * ratio) / 2;
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
        canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
            x, y, img.width * ratio, img.height * ratio);

    }
