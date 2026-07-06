# VoxTranslate

VoxTranslate is an academic prototype built to translate the spoken audio in an English video into a target language, generate translated subtitles, and merge the generated voice-over back with the original video.

This project was created as a third-year college project. It is best treated as a proof of concept rather than a production-ready video localization tool.

## What It Does

The intended pipeline is:

1. Download a YouTube video using `yt-dlp`.
2. Extract the source audio from the video.
3. Split the audio into fixed-length chunks.
4. Transcribe English speech using Google Speech Recognition through the `SpeechRecognition` package.
5. Translate the transcript into a target language.
6. Generate translated speech using `gTTS`.
7. Create translated subtitle files.
8. Merge the translated audio with the muted original video using `ffmpeg`.
9. Play the final video with subtitles through VLC.

The prototype also includes a Flask-based web interface for entering a video URL and target language, viewing source and translated transcripts, searching transcript text, highlighting educational keywords, and clipping a section of the generated video.

## Features

- YouTube video download support
- Audio extraction and removal from the original video
- English speech-to-text transcription
- Text translation into a target language such as Tamil
- Target-language subtitle generation
- Target-language audio generation
- Audio/video merge into a translated video
- Simple Flask web UI
- Transcript search and keyword highlighting
- Basic video clipping endpoint

## Tech Stack

- Python
- Flask
- yt-dlp
- pydub
- SpeechRecognition
- translate
- gTTS
- MoviePy
- ffmpeg
- VLC
- HTML, CSS, JavaScript, jQuery

## Project Structure

```text
voxtranslate/
|-- app.py              # Flask server and API routes
|-- pro.py              # Main video, audio, subtitle, translation, and merge pipeline
|-- psg.html            # Web interface
|-- requirements.txt    # Python dependencies
|-- video.mp4           # Sample/source video artifact
|-- original_video.mp4  # Muted video artifact
|-- out.mp3             # Extracted audio artifact
|-- subtitles.srt       # Source transcript subtitle artifact
|-- output_tamil.srt    # Translated subtitle artifact
|-- merged_audio.mp3    # Generated translated audio artifact
`-- merged_video.mp4    # Final merged video artifact
```

## Current Status

This repository is currently an archived prototype. The original implementation was built around a local Windows setup and contains hardcoded Windows paths in `app.py` and `pro.py`.

This checkout has a Python 3.13 virtual environment, but the project has not been fully modernized or validated on Python 3.13 yet. The dependencies need to be installed before running the app, and `ffmpeg` must be available on PATH.

Because of those issues, the project may not run successfully without maintenance.

## Known Limitations

- Audio, subtitles, and video can go out of sync after roughly 20 seconds.
- The pipeline uses fixed 10-second transcription chunks, so sentence boundaries are not preserved well.
- Generated translated speech can be longer or shorter than the original speech, which causes timing drift.
- Subtitle timing is copied from the source chunks rather than recalculated from generated speech duration.
- Several file paths are hardcoded for the original developer machine.
- The translation, transcription, and TTS steps depend on external online services.
- Error handling is minimal because this was built as a college prototype.
- The UI and backend are tightly coupled to local generated files.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install system dependencies:

```bash
brew install ffmpeg
brew install --cask vlc
```

On Windows, install `ffmpeg` and VLC manually, then update the hardcoded paths in `pro.py`.

## Running The Prototype

Start the Flask app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Before running the full conversion flow, update the hardcoded paths in:

- `app.py`
- `pro.py`

The current code references paths such as:

```text
C:\Users\vipur\nba-project\
C:\Program Files (x86)\VideoLAN\VLC\vlc.exe
```

These need to be changed to valid paths on the machine running the project.

## Why Sync Fails

The main sync issue comes from the way the prototype builds translated audio. It splits source audio into fixed chunks, translates the recognized text, generates new speech for each translated chunk, and concatenates the generated speech. Since translated speech duration rarely matches the source duration, the final voice-over gradually drifts away from the video and subtitle timings.

A stronger version would need forced alignment, per-segment duration control, silence padding, subtitle retiming, or a TTS system that can match target durations.

## Possible Improvements

- Replace hardcoded paths with configuration values.
- Use `pathlib` for cross-platform file handling.
- Add a proper upload flow instead of depending only on YouTube URLs.
- Generate valid numbered SRT files.
- Align generated speech duration with source segment duration.
- Retiming subtitles based on actual generated audio length.
- Add job progress tracking for long-running conversions.
- Save outputs in a dedicated `outputs/` directory.
- Add tests for SRT parsing, timestamp formatting, and language-code lookup.
- Package the pipeline as a CLI or API service.

## Resume Summary

Built VoxTranslate, a Flask-based video localization prototype that downloads English videos, transcribes speech, translates transcripts into a target language, generates translated voice-over audio and subtitles, and merges the result back into the original video using Python, yt-dlp, SpeechRecognition, gTTS, MoviePy, and ffmpeg.
