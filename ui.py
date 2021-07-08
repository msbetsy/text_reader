"""The module is responsible for the graphical interface of all windows in application."""
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu

MAIN_FONT = ("courier new", 12)
FONT_5_WORDS = ("courier new", 14, "bold")


class TextReaderInterface:
    """This class can be used to convert text from files (*.txt , *.pdf, *.docx) to audio file (*.mp3) and to find 5
    most popular words in text (including or excluding stop words).
    """

    def __init__(self):
        """Constructor method."""
        self.window = tk.Tk()
        self.style = ttk.Style()

        self.window.title("Text Reader")
        self.window.geometry("610x540")
        self.window.resizable(False, False)

        # Styles
        self.style.configure('TFrame', background='#DEEEEA')
        self.style.configure('TLabelframe', background="#DEEEEA")
        self.style.configure('TLabel', background="#DEEEEA", font=MAIN_FONT)
        self.style.configure('TNotebook', background="#EEEEEE")
        self.style.configure('TButton', font=('courier new', 12, "bold"), foreground='#231E23')
        self.style.configure('TLabelframe.Label', font=('courier new', 14, "bold"), foreground="#39A6A3",
                             background="#DEEEEA")
        self.window.option_add('*TCombobox*Listbox.font', MAIN_FONT)

        # Menu bar: File, Edit and Help
        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        # File items in menu bar
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command="")
        self.file_menu.add_command(label="Save", command="")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command="")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit items in menu bar
        self.edit_menu = Menu(self.menu_bar, tearoff=0, postcommand="")
        self.edit_menu.add_command(label="Cut", command="")
        self.edit_menu.add_command(label="Copy", command="")
        self.edit_menu.add_command(label="Paste", command="")
        self.edit_menu.add_command(label="Delete", command="")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help items in menu bar
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command="")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Tkinter Notebook
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.pack(expand=1, fill="both")

        self.tab_read = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_read, text="Read file")

        self.tab_words = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_words, text="Top 5 words")

        # Label Frames
        self.read_frame = ttk.LabelFrame(self.tab_read, text="Convert text to audio")
        self.read_frame.grid(column=0, row=0, padx=20, pady=20, ipady=15)

        self.convert = ttk.Button(self.read_frame, text="Convert!", command="")
        self.convert.place(x=30, y=390)

        self.textbox = scrolledtext.ScrolledText(self.read_frame, width=60, height=20, wrap=tk.WORD,
                                                 font=("courier new", 10))
        self.textbox.insert(tk.END, "Write/Upload your text here")
        self.textbox.grid(column=0, row=1, columnspan=4, padx=30, pady=20)

        self.coding_label = ttk.Label(self.read_frame, text="Choose language", font=MAIN_FONT)
        self.coding_label.grid(column=0, row=0, pady=5)

        self.language = tk.StringVar()
        self.language_chosen = ttk.Combobox(self.read_frame, width=12, textvariable=self.language, font=MAIN_FONT,
                                            state="readonly")

        self.language_chosen.grid(column=1, row=0)

        self.words_frame = ttk.LabelFrame(self.tab_words, height=452, width=433, text="5 most popular words in text")
        self.words_frame.grid_propagate(0)
        self.words_frame.grid(column=0, row=0, padx=20, pady=20, ipadx=66)
        self.words_frame.grid_columnconfigure(0, weight=1)

        self.first_word = ttk.Label(self.words_frame, font=FONT_5_WORDS, foreground="#BF1363")
        self.first_word.grid(column=0, row=0, padx=10, pady=(40, 30))

        self.second_word = ttk.Label(self.words_frame, font=FONT_5_WORDS, foreground="#BF1363")
        self.second_word.grid(column=0, row=1, padx=10, pady=30)

        self.third_word = ttk.Label(self.words_frame, font=FONT_5_WORDS, foreground="#BF1363")
        self.third_word.grid(column=0, row=2, padx=10, pady=30)

        self.fourth_word = ttk.Label(self.words_frame, font=FONT_5_WORDS, foreground="#BF1363")
        self.fourth_word.grid(column=0, row=3, padx=10, pady=30)

        self.fifth_word = ttk.Label(self.words_frame, font=FONT_5_WORDS, foreground="#BF1363")
        self.fifth_word.grid(column=0, row=4, padx=10, pady=30)

