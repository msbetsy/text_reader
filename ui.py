"""The module is responsible for the graphical interface of all windows in application."""
import math
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from tkinter import messagebox as msg
from tkinter.filedialog import asksaveasfile, askopenfile
from files import FilesManager
from languages import languages

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
        self.file = FilesManager()

        self.window.title("Text Reader")
        self.window.geometry("610x540")
        self.window.resizable(False, False)
        self.window.iconbitmap('favicon.ico')

        self.text = None
        self.file_path = None
        self.words = []
        self.language = "english"

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
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_text)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit items in menu bar
        self.edit_menu = Menu(self.menu_bar, tearoff=0, postcommand=self.disable_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_command(label="Delete", command=self.delete_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help items in menu bar
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.msg_about)
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

        self.convert = ttk.Button(self.read_frame, text="Convert!",
                                  command=lambda: [self.convert_text(), self.find_5_words()])
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
        self.language_chosen["values"] = tuple(languages.keys())
        self.language_chosen.current(1)
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

    def msg_about(self):
        """Show about --> option in Menu bar - Help - About."""
        self.window.withdraw()
        msg.showinfo("About Text Reader",
                     "A Python GUI created to convert text from files to speech and describe the text in 5 most "
                     "popular words.")
        self.window.deiconify()

    def disable_menu(self):
        """Allows to disable commands in menu bar depending on the Frame."""
        if self.tab_control.index("current") == 0:
            self.edit_menu.entryconfigure('Cut', state="normal")
            self.edit_menu.entryconfigure('Paste', state="normal")
            self.edit_menu.entryconfigure('Delete', state="normal")
            self.file_menu.entryconfigure('Open', state="normal")
        elif self.tab_control.index("current") == 1:
            self.edit_menu.entryconfigure('Cut', state="disabled")
            self.edit_menu.entryconfigure('Paste', state="disabled")
            self.edit_menu.entryconfigure('Delete', state="disabled")
            self.file_menu.entryconfigure('Open', state="disabled")

    def cut_text(self):
        """Cut text."""
        text = ""
        try:
            text = self.textbox.get("sel.first", "sel.last")
            self.textbox.delete("sel.first", "sel.last")
        except tk.TclError:
            index = float(math.floor(float(self.textbox.index(tk.INSERT))))
            text = self.textbox.get(index, index + 1)
            self.textbox.delete(index, index + 1)
        finally:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)

    def copy_text(self):
        """Copy text to clipboard."""
        self.window.clipboard_clear()
        if self.tab_control.index("current") == 0:
            try:
                self.text = self.textbox.get("sel.first", "sel.last")
            except tk.TclError:
                self.text = self.textbox.get("1.0", tk.END)
            self.window.clipboard_append(self.text)
        elif self.tab_control.index("current") == 1:
            self.window.clipboard_append(self.words)

    def paste_text(self):
        """Paste text."""
        text_to_add = self.window.clipboard_get()
        self.textbox.insert(self.textbox.index(tk.INSERT), text_to_add)

    def delete_text(self):
        """Delete text."""
        try:
            self.textbox.delete("sel.first", "sel.last")
        except tk.TclError:
            self.textbox.delete("1.0", tk.END)
            self.text = None
            self.first_word.configure(text="")
            self.second_word.configure(text="")
            self.third_word.configure(text="")
            self.fourth_word.configure(text="")
            self.fifth_word.configure(text="")

    def open_file(self):
        """Load text from the computer --> option in Menu bar - File - Open."""
        files = [('Text Document', '*.txt'), ('PDF Document', '*.pdf'), ('Word Document', '*.docx')]
        text_file = askopenfile(mode='r', title="Open your file", filetypes=files,
                                defaultextension=files)
        if text_file is not None:
            self.file_path = text_file.name
            text_inside = self.file.load_file(text_file.name)
            text_file.close()
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert("1.0", text_inside)
            self.text = self.textbox

    def save_text(self):
        """Allows to save the text as txt file."""
        if self.tab_control.index("current") == 0:
            text = self.textbox.get("1.0", tk.END)
            if text is not None:
                files = [('Text Document', '*.txt')]
                text_file = asksaveasfile(title="Save your text as .txt", filetypes=files,
                                          defaultextension=files)
                if text_file is not None:
                    text_file.write(text)
                    text_file.close()
            else:
                msg.showwarning(title="Warning", message="There is no data to save!")

    def quit(self):
        """Exit the application."""
        self.window.quit()
        self.window.destroy()
        exit()

    def convert_text(self):
        """Convert text to audio file."""
        if msg.askyesno(message="Do you want to save audio file?"):
            text = self.textbox.get("1.0", tk.END)
            self.file.text = text
            files = [('Sound', '*.mp3')]
            mp3_file = asksaveasfile(title="Save your mp3 file", filetypes=files, defaultextension=files)
            if mp3_file is not None:
                self.file.convert_text_to_mp3(languages[self.language.get()], mp3_file.name)
            msg.showinfo(title="Text to audio", message="Done")

    def find_5_words(self):
        """Find the most 5 popular words in text."""
        self.clean_5_words()
        del self.words[:]
        text = self.textbox.get("1.0", tk.END)
        self.file.text = text
        self.words = self.file.find_top_5_words(self.language.get())
        words_count = len(self.words)
        if words_count == 0:
            self.first_word.configure("All words are stop words.")
        if words_count >= 1:
            self.first_word.configure(text=self.words[0])
        if words_count >= 2:
            self.second_word.configure(text=self.words[1])
        if words_count >= 3:
            self.third_word.configure(text=self.words[2])
        if words_count >= 4:
            self.fourth_word.configure(text=self.words[3])
        if words_count == 5:
            self.fifth_word.configure(text=self.words[4])
        msg.showinfo(title="top 5 words", message="5 words are found, check: Top 5 words")

    def clean_5_words(self):
        """Remove words from Top 5 words Frame."""
        self.first_word.configure(text="")
        self.second_word.configure(text="")
        self.third_word.configure(text="")
        self.fourth_word.configure(text="")
        self.fifth_word.configure(text="")


