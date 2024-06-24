import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import requests
import time

# Initialize recognizer and microphone globally
recognizer = sr.Recognizer()
microphone = sr.Microphone()

accumulated_text = ""
start_time = 0
timer_running = False
live_translation = False

def start_speech_to_text():
    global stop_listening, start_time, timer_running
    stop_listening = recognizer.listen_in_background(microphone, callback, phrase_time_limit=5)
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    live_translation_button.config(state=tk.DISABLED)
    start_time = time.time()
    timer_running = True
    update_timer()

def stop_speech_to_text():
    global accumulated_text, timer_running
    stop_listening(wait_for_stop=False)
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    live_translation_button.config(state=tk.NORMAL)
    timer_running = False
    timer_label.config(text="Elapsed Time: 00:00:00")

    if not live_translation:
        language_code = languages[input_language_var.get()]
        target_language_code = languages[target_language_var.get()]
        translated_text = translate_text(accumulated_text, language_code, target_language_code)
        if translated_text:
            translation_text.insert(tk.END, f"Translated text ({target_language_var.get()}): {translated_text}\n\n")
            translation_text.see(tk.END)
        else:
            translation_text.insert(tk.END, "Translation failed.\n\n")
            translation_text.see(tk.END)
    
    accumulated_text = ""

def callback(recognizer, audio):
    global accumulated_text
    try:
        language_code = languages[input_language_var.get()]
        text = recognizer.recognize_google(audio, language=language_code)
        print("You said: " + text)
        accumulated_text += " " + text
        transliteration_text.insert(tk.END, f"{text}\n")
        transliteration_text.see(tk.END)
        if live_translation:
            target_language_code = languages[target_language_var.get()]
            translated_text = translate_text(text, language_code, target_language_code)
            if translated_text:
                translation_text.insert(tk.END, f"{translated_text}\n")
                translation_text.see(tk.END)
            else:
                translation_text.insert(tk.END, "Live translation failed.\n\n")
                translation_text.see(tk.END)
    except sr.UnknownValueError:
        transliteration_text.insert(tk.END, "Google Speech Recognition could not understand audio\n\n")
        transliteration_text.see(tk.END)
    except sr.RequestError as e:
        transliteration_text.insert(tk.END, f"Could not request results from Google Speech Recognition service; {e}\n\n")
        transliteration_text.see(tk.END)

def translate_text(text, source_language, target_language):
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': f'{source_language}|{target_language}'
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        translated_text = data['responseData']['translatedText']
        return translated_text
    except KeyError:
        return None

def update_timer():
    if timer_running:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 100) % 100)
        timer_label.config(text=f"Elapsed Time: {minutes:02}:{seconds:02}:{milliseconds:02}")
        root.after(10, update_timer)  # update every 10 milliseconds for more precision

def toggle_live_translation():
    global live_translation
    live_translation = not live_translation
    if live_translation:
        live_translation_button.config(text="Live Translation: ON", bg='#007bff')
    else:
        live_translation_button.config(text="Live Translation: OFF", bg='#6c757d')

# List of language codes supported by MyMemory
languages = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az',
    'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg',
    'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl',
    'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr',
    'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu',
    'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he', 'Hindi': 'hi',
    'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id',
    'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn',
    'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky',
    'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb',
    'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt',
    'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne',
    'Norwegian': 'no', 'Nyanja (Chichewa)': 'ny', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl',
    'Portuguese (Portugal, Brazil)': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
    'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd',
    'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es',
    'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tagalog (Filipino)': 'tl', 'Tajik': 'tg',
    'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk',
    'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh',
    'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
}

# Create the main window
root = tk.Tk()
root.title("Speech to Text Translator")
root.geometry("1000x600")
root.configure(bg='#f0f0f0')

# Maximize the window
root.state('zoomed')  # This maximizes the window on most systems

# Styles
label_font = ("Helvetica", 14)
menu_font = ("Helvetica", 12)
button_font = ("Helvetica", 16, "bold")
result_font = ("Helvetica", 14, "italic")
branding_font = ("Helvetica", 10, "italic")

# Create and place the widgets
frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=10)

input_language_var = tk.StringVar(value='English')
target_language_var = tk.StringVar(value='Spanish')

input_label = tk.Label(frame, text="Select input language:", font=label_font, bg='#f0f0f0')
input_label.pack(side=tk.LEFT, padx=10)

input_language_menu = ttk.Combobox(frame, textvariable=input_language_var, values=list(languages.keys()), font=menu_font)
input_language_menu.pack(side=tk.LEFT, padx=10)

target_label = tk.Label(frame, text="Select target language:", font=label_font, bg='#f0f0f0')
target_label.pack(side=tk.LEFT, padx=10)

target_language_menu = ttk.Combobox(frame, textvariable=target_language_var, values=list(languages.keys()), font=menu_font)
target_language_menu.pack(side=tk.LEFT, padx=10)

button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", font=button_font, command=start_speech_to_text, bg='#28a745', fg='white')
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="Stop", font=button_font, command=stop_speech_to_text, bg='#dc3545', fg='white', state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=10)

live_translation_button = tk.Button(button_frame, text="Live Translation: OFF", font=button_font, command=toggle_live_translation, bg='#6c757d', fg='white')
live_translation_button.pack(side=tk.LEFT, padx=10)

# Personal branding label
branding_label = tk.Label(root, text="Made by Jaffer Al Jaralla", font=branding_font, bg='#f0f0f0', fg='#6c757d')
branding_label.place(relx=0.95, rely=0.03, anchor=tk.NE)

# Add email address beneath the personal branding label
email_label = tk.Label(root, text="aljarallajaffer@gmail.com", font=branding_font, bg='#f0f0f0', fg='#6c757d')
email_label.place(relx=0.95, rely=0.06, anchor=tk.NE)

# Timer label
timer_label = tk.Label(root, text="Elapsed Time: 00:00:00", font=label_font, bg='#f0f0f0')
timer_label.pack(pady=10)

# Frame for the transliteration text and scrollbar
transliteration_frame = tk.Frame(root, bg='#f0f0f0')
transliteration_frame.pack(side=tk.LEFT, padx=10, pady=20, fill=tk.BOTH, expand=True)

transliteration_label = tk.Label(transliteration_frame, text="Transliteration", font=label_font, bg='#f0f0f0')
transliteration_label.pack()

# Text widget for displaying the transliterations
transliteration_text = tk.Text(transliteration_frame, font=result_font, wrap=tk.WORD, bg='#f0f0f0')
transliteration_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the transliteration text
transliteration_scrollbar = tk.Scrollbar(transliteration_frame, command=transliteration_text.yview)
transliteration_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
transliteration_text.config(yscrollcommand=transliteration_scrollbar.set)

# Frame for the translation text and scrollbar
translation_frame = tk.Frame(root, bg='#f0f0f0')
translation_frame.pack(side=tk.RIGHT, padx=10, pady=20, fill=tk.BOTH, expand=True)

translation_label = tk.Label(translation_frame, text="Translation", font=label_font, bg='#f0f0f0')
translation_label.pack()

# Text widget for displaying the translations
translation_text = tk.Text(translation_frame, font=result_font, wrap=tk.WORD, bg='#f0f0f0')
translation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the translation text
translation_scrollbar = tk.Scrollbar(translation_frame, command=translation_text.yview)
translation_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
translation_text.config(yscrollcommand=translation_scrollbar.set)

# Start the Tkinter event loop
root.mainloop()
