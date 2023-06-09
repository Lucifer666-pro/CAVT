from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import speech_recognition as sr
from googletrans import Translator
from moviepy.editor import *
import nltk
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cavt")
def cavt():
    return render_template('cavt.html')

@app.route("/example")
def example():
    return render_template('example.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    initial_language = request.form['initial_language']
    final_language = request.form['final_language']

    def download_youtube_video(youtube_link):
        yt = YouTube(youtube_link)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = 'youtube_video.mp4'
        video.download(output_path='.', filename='youtube_video.mp4')
        return video_path

    # Check if a file was uploaded or a YouTube link was provided
    if file:
        # Save the uploaded video file
        video_path = 'uploaded_video.mp4'
        file.save(video_path)
    else:
        # Extract the YouTube link from the form data
        youtube_link = request.form['youtube_link']

        # Download the YouTube video
        video_path = download_youtube_video(youtube_link)

    # Perform translation
    translated_video_path = video_to_translate(video_path, initial_language, final_language)

    # Return the translated video
    return send_file(translated_video_path, as_attachment=True)

def translate_text(text, source_lang, target_lang):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src=source_lang, dest=target_lang)
    return translation.text

def video_to_translate(video_path, initial_language, final_language):
    videoclip = VideoFileClip(video_path)
    videoclip.audio.write_audiofile("test.wav", codec='pcm_s16le')

    r = sr.Recognizer()

    lang_in = get_language_code(initial_language)
    lang_out = get_language_code(final_language)

    with sr.AudioFile("test.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=lang_in)

    # Split text into sentences/segments
    sentences = nltk.sent_tokenize(text)

    translated_sentences = []
    for sentence in sentences:
        trans = translate_text(sentence, lang_in, lang_out)
        translated_sentences.append(trans)

    translated_text = ' '.join(translated_sentences)

    myobj = gTTS(text=translated_text, lang=lang_out, slow=True)
    myobj.save("audio.wav")

    audioclip = AudioFileClip("audio.wav")

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip

    translated_video_path = "translated_video.mp4"
    videoclip.write_videofile(translated_video_path)

    return translated_video_path

def get_language_code(language):
    language_codes = {
        "English": "en",
	"Hindi": "hi",
	"Malayalam": "ml",
	"Tamil": "ta",
	"Telugu": "te",
	"Spanish": "es",
	"Portuguese": "pt",	
	"Japanese": "ja",
	"French": "fr",
	"German": "de",

    }
    return language_codes[language]


if __name__ == '__main__':
    nltk.download('punkt')
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
