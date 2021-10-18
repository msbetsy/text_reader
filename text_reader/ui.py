"""The module is responsible for the graphical interface of all windows in application."""
import math
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from tkinter import messagebox as msg
from tkinter.filedialog import asksaveasfile, askopenfile
from threading import Thread
from .files import FilesManager
from .database import SQLDatabase
from .languages import languages
from .tips import create_tip

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
        self.window.iconbitmap('text_reader/favicon.ico')

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
        self.file_menu.add_command(label="Open", command=self.open_thread)
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

        self.convert = ttk.Button(self.read_frame, text="Convert!", command=self.convert_thread)
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

        create_tip(self.language_chosen, "Choose the language of the text \nif you don't want to include stop words")

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
        """Allows to save the text as txt file or in SQL base depending on the Frame."""
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
        elif self.tab_control.index("current") == 1:
            text = self.words
            if len(text) > 0:
                result = msg.askyesno(title="Save words", message="Do you want to save top 5 words in SQL database?")
                if result:
                    if self.file_path is not None:
                        TextReaderInterface.start_sql_gui(words=text, path=self.file_path)
                    else:
                        msg.showwarning(message="You have to save your file as txt before saving in SQL!")
                        files = [('Text Document', '*.txt')]
                        text_file = asksaveasfile(title="Save your text as .txt", filetypes=files,
                                                  defaultextension=files)
                        if text_file is not None:
                            self.file_path = text_file.name
                            text_file.write(str(text))
                            text_file.close()
                            TextReaderInterface.start_sql_gui(words=text, path=self.file_path)
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

    def convert_thread(self):
        """Run methods in threads when convert button is clicked."""
        thread_mp3 = Thread(target=self.convert_text)
        thread_mp3.setDaemon(True)
        thread_mp3.start()
        thread_words = Thread(target=self.find_5_words)
        thread_words.setDaemon(True)
        thread_words.start()
        thread_clean_5_words = Thread(target=self.clean_5_words)
        thread_clean_5_words.setDaemon(True)
        thread_clean_5_words.start()

    def open_thread(self):
        """Run open method in threads during file opening."""
        thread_open_file = Thread(target=self.open_file)
        thread_open_file.setDaemon(True)
        thread_open_file.start()

    @staticmethod
    def start_sql_gui(words, path):
        """Open SQL GUI.

        :param words: 5 top popular words in text.
        :type: list
        :param path: File path to text in computer.
        :type: str
        """
        sql_gui = SQLSaveInterface(words=words, path=path)
        sql_gui.sql_window.mainloop()


class SQLSaveInterface(TextReaderInterface):
    """This class can be used to save 5 words in SQL database and for the creation new databases and tables.
    """

    def __init__(self, words, path):
        """Constructor method."""

        self.sql_window = tk.Toplevel()
        self.sql_window.title("Save in SQL base")
        self.sql_window.geometry("830x640")
        self.sql_window.resizable(False, False)
        self.sql_window.iconbitmap('text_reader/favicon.ico')
        self.words_to_use = words
        self.path = path

        self.sql_database = SQLDatabase()
        self.db = ""
        self.table_db = ""

        # Styles
        self.sql_window.configure(bg='#DEEEEA')
        self.sql_window.option_add('*TCombobox*Listbox.font', MAIN_FONT)

        # DB
        self.db_frame = ttk.LabelFrame(self.sql_window, height=105, width=650, text="Choose Database")
        self.db_frame.grid_propagate(0)
        self.db_frame.grid(column=0, row=0, padx=20, pady=20, ipadx=66)
        self.db_frame.grid_columnconfigure(0, weight=0)

        self.label_choose_db = ttk.Label(self.db_frame, text="Choose database from list:")
        self.label_choose_db.grid(column=0, row=0, pady=5)

        self.button_choose_db = ttk.Button(self.db_frame, text="Confirm", command=self.confirm_db)
        self.button_choose_db.grid(column=2, row=0, pady=5)

        self.database = tk.StringVar()
        self.database_chosen = ttk.Combobox(self.db_frame, width=30, textvariable=self.database, font=MAIN_FONT,
                                            state="readonly")
        self.show_db_combobox()
        self.database_chosen.grid(column=1, row=0, pady=5)

        self.label_create_db = ttk.Label(self.db_frame, text="Or create new one:")
        self.label_create_db.grid(column=0, row=1, pady=5)

        new_db = tk.StringVar()
        self.name_db = ttk.Entry(self.db_frame, textvariable=new_db, font=MAIN_FONT, width=32)
        self.name_db.grid(column=1, row=1, pady=5)

        self.button_create_db = ttk.Button(self.db_frame, text="Add new database", command=self.add_db)
        self.button_create_db.grid(column=2, row=1, pady=5)

        # Tables
        self.table_frame = ttk.LabelFrame(self.sql_window, height=105, width=650, text="Choose Table")
        self.table_frame.grid_propagate(0)
        self.table_frame.grid_columnconfigure(0, weight=0)
        self.table_frame.grid(column=0, row=1, padx=20, pady=20, ipadx=66)
        self.table_frame.grid_forget()

        self.label_choose_table = ttk.Label(self.table_frame, text="Choose table from list:")
        self.label_choose_table.grid(column=0, row=0, pady=5)

        self.button_choose_table = ttk.Button(self.table_frame, text="Confirm", command=self.confirm_table)
        self.button_choose_table.grid(column=2, row=0, pady=5)

        self.table = tk.StringVar()
        self.table_chosen = ttk.Combobox(self.table_frame, width=30, textvariable=self.table, font=MAIN_FONT,
                                         state="readonly")
        self.table_chosen.grid(column=1, row=0, pady=5)

        self.label_create_table = ttk.Label(self.table_frame, text="Or create new one:")
        self.label_create_table.grid(column=0, row=1, pady=5)

        new_table = tk.StringVar()
        self.name_table = ttk.Entry(self.table_frame, textvariable=new_table, font=MAIN_FONT, width=32)
        self.name_table.grid(column=1, row=1, pady=5)

        self.button_create_table = ttk.Button(self.table_frame, text="Add new table", command=self.create_table_db)
        self.button_create_table.grid(column=2, row=1, pady=5)

        # Words
        self.words_frame = ttk.LabelFrame(self.sql_window, height=270, width=650, text="Check words spelling")
        self.words_frame.grid_propagate(0)
        self.words_frame.grid_columnconfigure(0, weight=0)
        self.words_frame.grid(column=0, row=2, padx=20, pady=20, ipadx=66)
        self.words_frame.grid_forget()

        word_1 = tk.StringVar()
        self.word_1 = ttk.Entry(self.words_frame, font=FONT_5_WORDS, textvariable=word_1)
        self.word_1.grid(column=0, row=0, pady=10, padx=10)

        word_2 = tk.StringVar()
        self.word_2 = ttk.Entry(self.words_frame, font=FONT_5_WORDS, textvariable=word_2)
        self.word_2.grid(column=0, row=1, pady=10, padx=10)

        word_3 = tk.StringVar()
        self.word_3 = ttk.Entry(self.words_frame, font=FONT_5_WORDS, textvariable=word_3)
        self.word_3.grid(column=0, row=2, pady=10, padx=10)

        word_4 = tk.StringVar()
        self.word_4 = ttk.Entry(self.words_frame, font=FONT_5_WORDS, textvariable=word_4)
        self.word_4.grid(column=0, row=3, pady=10, padx=10)

        word_5 = tk.StringVar()
        self.word_5 = ttk.Entry(self.words_frame, font=FONT_5_WORDS, textvariable=word_5)
        self.word_5.grid(column=0, row=4, pady=10, padx=10)

        self.button_words_db = ttk.Button(self.words_frame, text="Save to database", command=self.save_in_db)
        self.button_words_db.grid(column=1, row=4)

    def confirm_db(self):
        """Confirm the database which will be used."""
        self.words_frame.grid_forget()
        self.table_frame.grid(column=0, row=1, padx=20, pady=20, ipadx=66)
        self.table_chosen.set("")
        self.show_table_combobox()

    def show_table_combobox(self):
        """Show all tables in chosen databases in combobox."""
        self.table_chosen["values"] = self.sql_database.show_tables(self.change_db())
        if len(self.table_chosen["values"]) > 0:
            self.table_chosen.current(0)

    def change_db(self):
        """Change database which will be used.

        :return: Name of database which will be used.
        :rtype: str
        """
        self.db = self.database.get()
        return self.db

    def add_db(self):
        """Create new SQL database."""
        name_db = self.name_db.get()
        if len(name_db) > 0:
            self.sql_database.db_name = name_db
            if self.sql_database.create_database():
                msg.showinfo(
                    message="".join(
                        [str(self.name_db.get()), " created as text_reader_", str(self.sql_database.db_name)]))
                self.name_db.delete(0, tk.END)
                self.show_db_combobox()
            else:
                msg.showinfo(message="Failed")
        else:
            msg.showinfo(message="Write db name!")

    def show_db_combobox(self):
        """Show all databases in combobox."""
        self.database_chosen["values"] = self.sql_database.show_database()
        if len(self.database_chosen["values"]) > 0:
            self.database_chosen.current(0)

    def confirm_table(self):
        """Confirm the table in the database which will be used."""
        self.words_frame.grid(column=0, row=2, padx=20, pady=20, ipadx=66)
        self.words_frame.grid_propagate(0)
        self.words_frame.grid_columnconfigure(0, weight=0)
        self.load_words()
        self.table_db = self.table.get()
        self.db = self.database.get()

    def create_table_db(self):
        """Create a new table in chosen database."""
        table_name = self.name_table.get()
        if len(table_name) > 0:
            self.table_db = table_name
            self.sql_database.db_name = self.db
            if self.sql_database.create_table(self.table_db):
                msg.showinfo(
                    message="".join([str(self.table_db), " created"]))
                self.name_table.delete(0, tk.END)
                self.show_table_combobox()
            else:
                msg.showinfo(message="Failed")
        else:
            msg.showinfo(message="Write table name!")

    def delete_words(self):
        """Remove 5 top words."""
        self.word_1.delete(0, tk.END)
        self.word_2.delete(0, tk.END)
        self.word_3.delete(0, tk.END)
        self.word_4.delete(0, tk.END)
        self.word_5.delete(0, tk.END)

    def load_words(self):
        """Load top 5 words from text to GUI."""
        self.delete_words()
        words_count = len(self.words_to_use)
        if words_count >= 1:
            self.word_1.insert(0, self.words_to_use[0])
        if words_count >= 2:
            self.word_2.insert(0, self.words_to_use[1])
        else:
            self.word_2.configure(state="disabled")
        if words_count >= 3:
            self.word_3.insert(0, self.words_to_use[2])
        else:
            self.word_3.configure(state="disabled")
        if words_count >= 4:
            self.word_4.insert(0, self.words_to_use[3])
        else:
            self.word_4.configure(state="disabled")
        if words_count == 5:
            self.word_5.insert(0, self.words_to_use[4])
        else:
            self.word_5.configure(state="disabled")

    def save_in_db(self):
        """Save 5 top words in chosen table."""
        self.sql_database.table_name = self.table_db
        self.sql_database.db_name = self.db
        if self.sql_database.insert_item(text_path=self.path, word_first=self.word_1.get(),
                                         word_second=self.word_2.get(),
                                         word_third=self.word_3.get(), word_fourth=self.word_4.get(),
                                         word_fifth=self.word_5.get()):
            msg.showinfo(message="Done")
