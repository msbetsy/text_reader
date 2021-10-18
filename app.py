"""This module initializes the start of the program."""
from text_reader.ui import TextReaderInterface

if __name__ == '__main__':
    app = TextReaderInterface()
    app.window.mainloop()
