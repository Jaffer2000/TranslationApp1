import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import requests

def speech_to_text(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language_code)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

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

def start_translation():
    input_language_name = input_language_var.get()
    target_language_name = target_language_var.get()
    
    source_language_code = languages[input_language_name]
    target_language_code = languages[target_language_name]
    
    text = speech_to_text(source_language_code)
    if text:
        translated_text = translate_text(text, source_language_code, target_language_code)
        if translated_text:
            result_label.config(text="Translated text: " + translated_text)
        else:
            messagebox.showerror("Error", "Translation failed.")
    else:
        messagebox.showerror("Error", "Speech to text conversion failed.")

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
root.geometry("800x600")
root.configure(bg='#f0f0f0')

# Styles
label_font = ("Helvetica", 14)
menu_font = ("Helvetica", 12)
button_font = ("Helvetica", 16, "bold")
result_font = ("Helvetica", 18, "italic")

# Create and place the widgets
frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=20)

input_language_var = tk.StringVar(value='English')
target_language_var = tk.StringVar(value='Spanish')

input_label = tk.Label(frame, text="Select input language:", font=label_font, bg='#f0f0f0')
input_label.pack(side=tk.LEFT, padx=10)

input_language_menu = tk.OptionMenu(frame, input_language_var, *languages.keys())
input_language_menu.config(font=menu_font)
input_language_menu.pack(side=tk.LEFT, padx=10)

target_label = tk.Label(frame, text="Select target language:", font=label_font, bg='#f0f0f0')
target_label.pack(side=tk.LEFT, padx=10)

target_language_menu = tk.OptionMenu(frame, target_language_var, *languages.keys())
target_language_menu.config(font=menu_font)
target_language_menu.pack(side=tk.LEFT, padx=10)

translate_button = tk.Button(root, text="Translate Speech", font=button_font, command=start_translation, bg='#007BFF', fg='white')
translate_button.pack(pady=20)

result_label = tk.Label(root, text="", font=result_font, wraplength=800, bg='#f0f0f0')
result_label.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
