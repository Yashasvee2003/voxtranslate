import os
import yt_dlp
from pydub import AudioSegment
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import time
from datetime import datetime
from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
# ffmpeg_directory = r'C:\Users\vipur\Downloads\ffmpeg-6.0'
ffmpeg_directory = r"C:\ffmpeg"
os.environ['PATH'] += os.pathsep + ffmpeg_directory
#getting the language code
global transcript
global to_transcript

def get_language_code(language_name):
    language_dict = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar',
    'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be',
    'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
    'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn',
    'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr',
    'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi',
    'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka',
    'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
    'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi',
    'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig',
    'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
    'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km',
    'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo',
    'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb',
    'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml',
    'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn',
    'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or',
    'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt',
    'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm',
    'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn',
    'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl',
    'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw',
    'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th',
    'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug',
    'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
    'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'

    }
    return language_dict.get(language_name.lower())

#video generation code


# URL of the YouTube video
def download_video(url,target_language):
    target_language=get_language_code(target_language)
    print(target_language)
    video_url = url

    # Options for the download
    options = {
        'format': 'best',  # Download the best available quality
        'outtmpl': 'video.%(ext)s',  # Save path and filename
    }

    # Create a YoutubeDL object
    ydl = yt_dlp.YoutubeDL(options)

    # Download the video
    ydl.download([video_url])
    remove_audio(url,target_language)

    print('Download complete!')
def remove_audio(url,target_language):
    video_path = r"C:\Users\vipur\nba-project\video.mp4"
    output_path = r"C:\Users\vipur\nba-project\original_video.mp4"
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Set the audio to None, effectively removing audio
    video_clip = video_clip.set_audio(None)
    
    # Save the video with no audio
    video_clip.write_videofile(output_path)
    download_audio(url,target_language)



#audio genertaion code


def download_audio(url,target_language):
    output_path=r'C:\Users\vipur\nba-project'
    file_name="out"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Set the preferred codec to WAV
            'preferredquality': '192',  # Adjust quality if needed
        }],
        'outtmpl': os.path.join(output_path, f"{file_name}.%(ext)s"),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file_path = os.path.join(output_path, f"{file_name}.mp3")
    generate_srt(url,target_language)
    print("audio download completed")
    
#code for generating subtitles

def split_audio(audio_path, chunk_duration_ms):
    audio = AudioSegment.from_file(audio_path)
    chunks = [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)]
    return chunks

def transcribe_audio(audio_chunk):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk.export(format="wav")) as source:
        audio = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio)
        return transcript
    except sr.UnknownValueError:
        return ""

def generate_srt(url,target_language):
    audio_path = "out.mp3"
    chunk_duration_ms = 10000  # Split audio into 10-second chunks
    audio_chunks = split_audio(audio_path, chunk_duration_ms)

    subtitles = []

    for idx, chunk in enumerate(audio_chunks):
        transcript = transcribe_audio(chunk)
        start_time = idx * (chunk_duration_ms / 1000)
        end_time = (idx + 1) * (chunk_duration_ms / 1000)
        subtitles.append((start_time, end_time, transcript))
    srt_file_path = "subtitles.srt"
    with open(srt_file_path, "w") as f:
        for idx, subtitle in enumerate(subtitles):
            start_time, end_time, text = subtitle
            #f.write(f"{idx + 1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
    translate_srt(url,target_language)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

#code for translating the srt file

def translate_srt(url,target_language):
    input_file = 'subtitles.srt'  # Replace with your input SRT file
    output_file = 'output_tamil.srt'  # Replace with the desired output file name
    source_lang = 'en' 
    translator = Translator(to_lang=target_language, from_lang=source_lang)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    translated_lines = []
    for line in lines:
        if line.strip().isdigit() or '-->' in line:
            translated_lines.append(line)  # Keep line numbers and timecodes unchanged
        else:
            translation = translator.translate(line.strip())
            translated_lines.append(translation + '\n')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
    generate_and_merge_audio_from_srtf( url,target_language)
    print("Translation complete. Output written to")

#generating audio and merging the audio


# Read the SRTF file and parse timings and subtitles
def parse_srtf_file(file_path, encoding="utf-8"):
    timings = []
    subtitles = []
    
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.read().splitlines()
        i = 0
        while i < len(lines):
            if "-->" in lines[i]:  # Check if this line contains the timestamp
                timing = lines[i]
                i += 1
                subtitle = []
                while i < len(lines) and lines[i].strip():  # Read subtitle text until an empty line is encountered
                    subtitle.append(lines[i])
                    i += 1
                subtitles.append('\n'.join(subtitle))
                timings.append(timing)
            else:
                i += 1
    
    return timings, subtitles

# Convert SRTF timestamp to seconds
def convert_srtf_time_to_seconds(srtf_time):
    start_time_str, _ = srtf_time.split(" --> ")
    start_time = datetime.strptime(start_time_str, "%H:%M:%S,%f")
    total_seconds = (start_time - datetime.min).total_seconds()
    
    return int(total_seconds)

# Main function to generate and merge audio files
def generate_and_merge_audio_from_srtf( url,target_language):
    file_path = "output_tamil.srt"
    timings, subtitles = parse_srtf_file(file_path)
    
    audio_segments = []  # To store audio segments
    
    for i in range(len(timings)):
        start_time = convert_srtf_time_to_seconds(timings[i])
        current_time = time.time()
        
        sleep_duration = max(start_time - current_time, 0)
        sleep_duration = 10
        subtitle = subtitles[i]
        
        if subtitle:
            tts = gTTS(subtitle, lang=target_language)
            audio_path = f"audio_{i}.mp3"
            tts.save(audio_path)
            
            print(f"Generated audio for subtitle '{subtitle}' at time {start_time} seconds")
            time.sleep(sleep_duration)
            
            audio_segment = AudioSegment.from_mp3(audio_path)
            audio_segments.append(audio_segment)
            
            os.remove(audio_path)
        else:
            silence_duration = int(sleep_duration * 1000)
            silent_segment = AudioSegment.silent(duration=silence_duration)
            audio_segments.append(silent_segment)
    
    merged_audio = AudioSegment.empty()
    for audio_segment in audio_segments:
        merged_audio += audio_segment
    
    merged_audio.export("merged_audio.mp3", format="mp3")
    merge_audio_video()


#merging audio with video


def merge_audio_video():
    video_path = r"C:\Users\vipur\nba-project\original_video.mp4"  # Replace with your input video file
    audio_path = r"C:\Users\vipur\nba-project\merged_audio.mp3"
    output_path = r"C:\Users\vipur\nba-project\merged_video.mp4"  # Output path for the merged video
    merge_command = [
        "ffmpeg",  # Use the command 'ffmpeg' (since it's now in PATH)
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",  # Copy video codec
        "-c:a", "aac",   # AAC audio codec
        "-strict", "experimental",  # Use experimental codecs
        output_path
    ]
    result = subprocess.run(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print('Merge complete!')
    print('--- Output ---')
    print(result.stdout)
    print('--- Errors ---')
    print(result.stderr)
    print('Merge complete!')
    play_vlc()
    

def play_vlc():
    vlc_executable_path = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    video_path = r"C:\Users\vipur\nba-project\merged_video.mp4"
    subtitles_path = r"C:\Users\vipur\nba-project\output_tamil.srt"
    command = [
        vlc_executable_path,
        video_path,
        "--sub-file", subtitles_path
    ]
    subprocess.run(command)
def read_file(file_path):
    try:    
        with open(file_path, 'rb') as file:
            content = file.read()
            decoded_content=content.decode('utf-8')
        return decoded_content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"
from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_subvideo(input_path, output_path, start_time, end_time):
    video_clip = VideoFileClip(input_path).subclip(start_time, end_time)
    video_clip.write_videofile(output_path, codec='libx264')

