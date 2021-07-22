"""The module is responsible for the tips in the graphical interface."""
import tkinter


class TipManager:
    """This class can be used for creation tips in GUI.
    """

    def __init__(self, widget):
        """Constructor method.

        :param widget: Name of the widget which will contain a tip.
        :type: tkinter.ttk.widget
        """
        self.widget = widget
        self.tip_window = None

    def show_tip(self, text):
        """This method is responsible for the appearance and location of the tips.

        :param text: Text in a tip.
        :type: str
        """
        if self.tip_window or not text:
            return
        x, y, _w, h = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 10
        y = y + h + self.widget.winfo_rooty() + 10
        self.tip_window = tool_window = tkinter.Toplevel(self.widget)
        tool_window.wm_overrideredirect(True)
        tool_window.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(tool_window, text=text, justify=tkinter.CENTER,
                              bg="#EEEEEE", fg="#BF1363")
        label.pack(ipadx=3)

    def hide_tip(self):
        """This method is responsible for hiding the tips.
        """
        tool_window = self.tip_window
        self.tip_window = None
        if tool_window:
            tool_window.destroy()


def create_tip(widget, text):
    """This method is responsible for creation tips in the GUI."""
    new_tip = TipManager(widget)

    def enter(event):
        """Show tip."""
        new_tip.show_tip(text)

    def leave(event):
        """Hide tip."""
        new_tip.hide_tip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
