from langdetect import detect_langs
from googletrans import Translator

text = "Привет спасибо вам!"

# Xác định danh sách các ngôn ngữ có khả năng cao nhất
# languages = detect_langs(text)
# print(languages)
# likely_lang = languages[0].lang if languages else 'en'

# # Chuyển đổi văn bản sang tiếng Anh
# translator = Translator()
# translated_text = translator.translate(text, src=likely_lang, dest='en')
# english_text = translated_text.text

# print(english_text)

def src_lang(text):
    languages = detect_langs(text)
    likely_lang = languages[0].lang if languages else 'en'
    return likely_lang

def convert(text, lang):
    languages = detect_langs(text)
    likely_lang = languages[0].lang if languages else lang

    # Chuyển đổi văn bản sang tiếng Anh
    translator = Translator()
    translated_text = translator.translate(text, src=likely_lang, dest=lang)
    return translated_text.text

print(convert("hello! i go to school",lang='vi'))



# from googletrans import Translator
# translator = Translator()
# text = "Xin chào, cảm ơn bạn! tôi là phương"
# translation = translator.translate(text, src='vi', dest='en')
# print(translation.text)
