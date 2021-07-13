"""The module is responsible for the operations on files."""
import textract
import chardet


class FilesManager:
    """This class can be used for operations on files like loading them and for text operations.
    Example:
    from files import FilesManager
    file = FilesManager()
    file.load_file("text_file_to_tests.txt")
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
