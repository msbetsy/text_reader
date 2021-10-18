"""The module is responsible for the operations on files."""
from collections import OrderedDict
import string
import chardet
import textract
from gtts import gTTS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class FilesManager:
    """This class can be used for operations on files like loading them and for text operations.
    Example:
    from files import FilesManager
    file = FilesManager()
    file.load_file("text_file_to_tests.txt")
    file.convert_text_to_mp3("en","file.mp3")
    file.find_top_5_words("english")
    file.find_top_5_words("french")
    """

    def __init__(self):
        """Constructor method.
        """
        self.text = None
        self.top_5 = []

    def load_file(self, file):
        """Load file from computer.

        :param file: File path.
        :type: str
        :raises UnicodeDecodeError: Error with text coding.
        :return: Text from the file.
        :rtype: str
        """
        try:
            with open(file, encoding="utf-8") as f:
                self.text = f.read()
        except UnicodeDecodeError:
            text = textract.process(file)
            file_information = chardet.detect(text)
            self.text = text.decode(file_information["encoding"])

        return self.text

    def convert_text_to_mp3(self, language, filename):
        """Convert text to audio.

        :param language: Language of the text.
        :type: str
        :param filename: File path.
        :type: str
        """
        audio = gTTS(text=self.text, lang=language, slow=False)
        audio.save(filename)

    def find_top_5_words(self, language):
        """Find the 5 most popular words in text with of without stop words.

        :param language: Language of the file.
        :type: str
        :raises LookupError: No tokenizers installed.
        :return: The 5 most popular words in text.
        :rtype: list
        """
        del self.top_5[:]
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        finally:
            tokens = word_tokenize(self.text)
            tokens = [word.lower() for word in tokens]
            tokens_without_punctuation = [word for word in tokens if word not in string.punctuation]

        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        finally:
            if language == "other":
                all_words = tokens_without_punctuation
            else:
                stop_words = stopwords.words(language)
                all_words = [word for word in tokens_without_punctuation if word not in stop_words]

        wordcount = {key: 0 for key in all_words}
        for word in all_words:
            wordcount[word] += 1

        ordered_wordcount = OrderedDict((key, value) for (key, value) in sorted(wordcount.items(), key=lambda x: x[1]))

        for item in list(reversed(ordered_wordcount))[:5]:
            self.top_5.append(item)

        return self.top_5
