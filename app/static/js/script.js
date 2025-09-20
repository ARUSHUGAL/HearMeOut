const btnRec = document.getElementById("btn-record");
const btnStop = document.getElementById("btn-stop");
const btnAnalyzeText = document.getElementById("btn-analyze-text");
const manualText = document.getElementById("manual-text");
const hint = document.getElementById("hint");

const transcriptCard = document.getElementById("transcript-card");
const transcriptEl = document.getElementById("transcript");
const moodCard = document.getElementById("mood-card");
const emojiEl = document.getElementById("emoji");
const moodEl = document.getElementById("mood");
const tipEl = document.getElementById("tip");
const memeEl = document.getElementById("meme");
const playlistEl = document.getElementById("playlist");

let recog, isRecording = false, liveTranscript = "";

function supported(){
  return ("webkitSpeechRecognition" in window) || ("SpeechRecognition" in window);
}
function setup(){
  if(!supported()) return;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recog = new SR();
  recog.continuous = true;
  recog.interimResults = true;
  recog.lang = "en-US";

  recog.onresult = (e)=>{
    let txt = "";
    for(let i=e.resultIndex;i<e.results.length;i++){
      txt += e.results[i][0].transcript;
    }
    liveTranscript = txt;
    hint.textContent = "Listening… speak freely.";
  };
}
function startRec(){
  if(!supported()){
    hint.textContent = "Speech recognition not supported. Use the text box below.";
    return;
  }
  isRecording = true; liveTranscript = "";
  btnRec.disabled = true; btnStop.disabled = false;
  hint.textContent = "Listening…";
  recog.start();
}
function stopRec(){
  isRecording = false;
  btnRec.disabled = false; btnStop.disabled = true;
  try{ recog.stop(); }catch(_){}
  const text = (liveTranscript || "").trim();
  if(!text){
    hint.textContent = "No speech captured. Try again or type below.";
    return;
  }
  analyzeText(text);
}
async function analyzeText(text){
  hint.textContent = "Analyzing…";
  try{
    const res = await fetch("/analyze", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if(!res.ok) throw new Error(data.error || "Server error");

    transcriptEl.textContent = data.transcript;
    transcriptCard.classList.remove("hidden");

    emojiEl.textContent = data.emoji;
    moodEl.textContent = `${data.mood} (${data.confidence})`;
    tipEl.textContent = data.tip;

    if(data.meme_url){ memeEl.src = data.meme_url; memeEl.classList.remove("hidden"); }
    if(data.playlist_url){ playlistEl.href = data.playlist_url; playlistEl.classList.remove("hidden"); }

    moodCard.classList.remove("hidden");
    hint.textContent = "Done ✅";
  }catch(err){
    hint.textContent = "Error: " + err.message;
  }
}

// wire up
setup();
btnRec.addEventListener("click", startRec);
btnStop.addEventListener("click", stopRec);
btnAnalyzeText.addEventListener("click", ()=>{
  const t = manualText.value.trim();
  if(!t){ hint.textContent = "Type something first."; return; }
  analyzeText(t);
});
