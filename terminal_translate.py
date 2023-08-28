from translate import Translator

"""Simple terminal translator app: to French"""


def get_phrase():
    return input("Enter a word or phrase (X to end): ")


def translate():
    translator = Translator(to_lang="French")  # Change to whatever language you want.
    while True:
        phrase = get_phrase()
        if phrase.upper() == "X":
            break
        translated_text = translator.translate(phrase)
        print(translated_text)


translate()
