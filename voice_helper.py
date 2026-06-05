from gtts import gTTS
from io import BytesIO

def text_to_speech_audio(text):

    try:

        mp3_fp = BytesIO()

        tts = gTTS(
            text=text,
            lang="en"
        )

        tts.write_to_fp(mp3_fp)

        mp3_fp.seek(0)

        return mp3_fp.read()

    except Exception as e:

        print("TTS Error:", e)

        return None

def get_voice_input_component() -> str:
    """
    Returns an HTML string that renders a voice recorder widget
    using the browser's built-in Web Speech API.

    The recognized text is displayed and the user can click
    'Use This Question' which calls window.parent.postMessage
    so Streamlit can pick it up — OR the user simply copies
    the transcript into the text box above.

    Note: Works in Chrome/Edge. Firefox requires a flag.
          HTTPS (or localhost) is required for microphone access.
    """
    return """
<style>
  body { font-family: sans-serif; margin: 0; padding: 0; }
  #voice-box {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px;
    background: #0e1117;
    border-radius: 8px;
    border: 1px solid #333;
  }
  .btn-row { display: flex; gap: 8px; }
  button {
    padding: 6px 14px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
  }
  #startBtn  { background: #1f77b4; color: white; }
  #stopBtn   { background: #d62728; color: white; }
  #useBtn    { background: #2ca02c; color: white; }
  #transcript {
    min-height: 36px;
    color: #fafafa;
    font-size: 14px;
    padding: 6px 8px;
    background: #1a1d26;
    border-radius: 6px;
    word-wrap: break-word;
  }
  #status { color: #888; font-size: 12px; }
</style>

<div id="voice-box">
  <div class="btn-row">
    <button id="startBtn" onclick="startRecording()">Start Recording</button>
    <button id="stopBtn"  onclick="stopRecording()" disabled>Stop</button>
    <button id="useBtn"   onclick="useTranscript()" disabled>Use This Question</button>
  </div>
  <div id="transcript">Your spoken question will appear here…</div>
  <div id="status">Ready</div>
</div>

<script>
  let recognition = null;
  let finalTranscript = "";

  function startRecording() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      document.getElementById('status').textContent =
        'Transcript copied to clipboard. Paste into the Ask Neil box.';
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => {
      document.getElementById('status').textContent = 'Listening…';
      document.getElementById('startBtn').disabled = true;
      document.getElementById('stopBtn').disabled = false;
      document.getElementById('useBtn').disabled = true;
      finalTranscript = "";
    };

    recognition.onresult = (event) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interim += event.results[i][0].transcript;
        }
      }
      document.getElementById('transcript').textContent =
        finalTranscript + (interim ? ' ' + interim : '');
    };

    recognition.onend = () => {
      document.getElementById('status').textContent = 'Done — review and click "Use This Question"';
      document.getElementById('startBtn').disabled = false;
      document.getElementById('stopBtn').disabled = true;
      if (finalTranscript.trim()) {
        document.getElementById('useBtn').disabled = false;
      }
    };

    recognition.onerror = (e) => {
      document.getElementById('status').textContent = 'Error: ' + e.error;
      document.getElementById('startBtn').disabled = false;
      document.getElementById('stopBtn').disabled = true;
    };

    recognition.start();
  }

  function stopRecording() {
    if (recognition) recognition.stop();
  }

  function useTranscript() {
    const text = finalTranscript.trim();
    if (!text) return;
    // Send to Streamlit via postMessage — handled by Streamlit's component protocol
    window.parent.postMessage(
      { type: 'streamlit:setComponentValue', value: text },
      '*'
    );
    document.getElementById('status').textContent =
      'Copied to input above — press Ctrl+V to execute!';
    // Also copy to clipboard as fallback
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).catch(() => {});
    }
  }
</script>
"""