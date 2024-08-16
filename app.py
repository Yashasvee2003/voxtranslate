from flask import Flask, request, jsonify, send_file, render_template
from pro import read_file
from pro import download_video
from pro import extract_subvideo
from pro import play_vlc
from pro import merge_audio_video
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_index_html():
    return send_file('psg.html')

@app.route('/run_function', methods=['POST'])
def run_function():
    data = request.json
    print("Received Data:", data)
    parameter1 = data['parameter1']
    parameter2 = data['parameter2']
    #download_video(parameter1, parameter2)  # Get transcript content from play_vlc function
    #merge_audio_video()
    transcript_content = read_file(r"C:\Users\vipur\nba-project\subtitles.srt")
    target_transcript = read_file(r"C:\Users\vipur\nba-project\output_tamil.srt")
    play_vlc()
    return jsonify({
        "result": "Audio downloaded and saved in WAV format successfully.",
        "transcript": transcript_content,
        "to": target_transcript
    })
@app.route('/sub_video', methods=['POST'])
def sub_video():
    data = request.json
    print("Received Data:", data)
    parameter3 = data['parameter3']
    parameter4 = data['parameter4']
    extract_subvideo("merged_video.mp4", r"C:\Users\vipur\clippings\clip.mp4", parameter3, parameter4)
    return jsonify({
        "result": "video clipped.",
    })



if __name__ == '__main__':
    app.run(debug=True)