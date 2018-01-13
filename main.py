try:
    from tkinter import *
    from tkinter.ttk import *

    import pyevtx
except ImportError:
    print("Please run with Python 3")
    exit(0)

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.winfo_toplevel().title('PyEventLogViewer')
        self.minsize(width=800, height=600)

        self.log_file_area = LogFileEntry(self)
        self.log_file_button = LogFileButton(self)
        self.log_file_text = LogFileText(self)

        self.event_number_area = EventNumberEntry(self)
        self.event_number_button = EventNumberButton(self)

        self.text_area = TextArea(self)

        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def import_log(self):
        log_file = self.log_file_area.string_var.get()

        self.log = pyevtx.open(log_file)
        self.log_file_text.status.config(text='{} records in {}.'.format(self.log.get_number_of_records(), log_file))

        return

    def print_record(self):
        number = int(self.event_number_area.string_var.get())

        if number < 0 or number >= self.log.get_number_of_records():
            self.text_area.status.config(text="Please provide a record number that exists - not {}.".format(number))
            return

        self.text_area.status.config(text=self.log.get_record(number).xml_string)

        return


class TextArea(Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.status = Label(parent, text='', anchor="nw", *args, **kwargs)
        self.status.pack(fill=BOTH, side=TOP)


class LogFileEntry(Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.string_var = StringVar()

        self.entry = Entry(parent, textvariable=self.string_var)
        self.entry.pack(fill=X, side=TOP)


class LogFileButton(Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.button_import = Button(parent, text='Import EVTX File', command=self.master.import_log)
        self.button_import.pack(side=TOP)


class LogFileText(Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.status = Label(parent, text='Please import an EVTX File.', anchor="nw", *args, **kwargs)
        self.status.pack(fill=BOTH, side=TOP)


class EventNumberEntry(Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.string_var = StringVar()

        self.entry = Entry(parent, textvariable=self.string_var)
        self.entry.pack(fill=X, side=TOP)


class EventNumberButton(Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.button_import = Button(parent, text='Print Event', command=lambda: self.master.print_record())
        self.button_import.pack(side=TOP)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
