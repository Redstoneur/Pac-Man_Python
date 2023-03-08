import tkinter as tk


class MessageBox(tk.Tk):
    """
    Class MessageBox
    Description: Class to create a message box
    """

    def __init__(self, message):
        """
        Constructor of the class MessageBox
        :param message: message to display
        """
        super().__init__()
        self.title("Erreur")
        self.geometry("300x100")
        tk.Label(self, text=message).pack(padx=10, pady=10)
        tk.Button(self, text="OK", command=self.destroy).pack(padx=10, pady=10)
        self.mainloop()
