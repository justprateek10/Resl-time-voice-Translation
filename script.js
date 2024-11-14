// Assume we have methods startRecording() and stopRecording() to handle audio recording

let transcriptionText = "";
let translationText = "";

function startRecording() {
    // Start recording logic here
}

function stopRecording() {
    // Stop recording logic here and send the audio file to the Flask server

    var formData = new FormData();
    formData.append("audio", audioBlob);  // audioBlob is the audio file blob (ensure it's captured)

    $.ajax({
        url: "/translate",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            // Update transcription and translation results
            transcriptionText = response.transcription;
            translationText = response.translation;

            document.getElementById("transcription").textContent = transcriptionText;
            document.getElementById("translation").textContent = translationText;

            // Display transcription file path (optional)
            const transcriptionFilePath = response.transcription_file;
            document.getElementById("transcriptionFileLink").textContent = "Download Transcription";
            document.getElementById("transcriptionFileLink").href = transcriptionFilePath;
        },
        error: function(xhr, status, error) {
            console.error("Error in translation:", error);
        }
    });
}

function speakTranscription() {
    // Call text-to-speech API to speak the transcription
    if (transcriptionText) {
        const utterance = new SpeechSynthesisUtterance(transcriptionText);
        window.speechSynthesis.speak(utterance);
    }
}

function speakTranslation() {
    // Call text-to-speech API to speak the translation
    if (translationText) {
        const utterance = new SpeechSynthesisUtterance(translationText);
        window.speechSynthesis.speak(utterance);
    }
}
