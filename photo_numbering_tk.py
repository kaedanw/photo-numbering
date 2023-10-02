from pathlib import Path
import natsort
import tkinter as tk
from tkinter import messagebox

def tkmain():
    def submit():
        folder = folder_entry.get()
        extensions = []
        if jpg_var.get():
            extensions.append("JPG")
        if png_var.get():
            extensions.append("PNG")
        
        message1 = "Please confirm that you would like to renumber the photos\nfor the following folder and file extensions:-\n"
        message2 = f"Folder: {folder}\n\nExtensions: {', '.join(extensions)}"
        message = '\n'.join((message1, message2))
        confirmation = messagebox.askokcancel("Confirmation", message)
        
        if confirmation and extensions:
            message_label.config(text = "Renaming in progress..")
            photos = []
            for ext in extensions:
                photos.extend(Path(folder).glob(f'*.{ext}'))
            files = natsort.natsorted(photos, alg=natsort.PATH)
            uiRenumber(files)
        message_label.config(text = "Done.")
        print("Done.")

    def uiRenumber(files):
        for run in range(2):
            i = 0
            for file in (natsort.natsorted(files, alg=natsort.PATH)):
                i += 1
                photo = Path(file)
                if run == 0:
                    photo.rename(photo.parent / f'{i:03} tmp{photo.suffix}')
                    print(f'renamed {photo.name} -> {i}tmp')
                if run == 1:
                    photo = photo.parent / f'{i:03} tmp{photo.suffix}'
                    print(f'renamed {photo.name} -> {i}final')
                    photo.rename(photo.parent / f'{i:03}{photo.suffix}')

    root = tk.Tk()
    root.title("Photo Numbering")
    root.geometry("800x250")

    # Folder Entry
    folder_label = tk.Label(root, text="Folder:")
    folder_label.pack()

    folder_entry = tk.Entry(root)
    folder_entry.pack(fill=tk.X)

    # Extension Checkboxes
    extension_label = tk.Label(root, text="Extension:")
    extension_label.pack()

    jpg_var = tk.BooleanVar()
    jpg_checkbox = tk.Checkbutton(root, text="JPG", variable=jpg_var, onvalue=True, offvalue=False)
    jpg_checkbox.select()
    jpg_checkbox.pack(anchor='center')

    png_var = tk.BooleanVar()
    png_checkbox = tk.Checkbutton(root, text="PNG", variable=png_var, onvalue=True, offvalue=False)
    png_checkbox.pack(anchor='center')

    # Submit Button
    submit_button = tk.Button(root, text="Renumber Photos", command=submit)
    submit_button.pack()

    message_label = tk.Label(root, text="")
    message_label.pack()
    
    folder_entry.bind("<FocusIn>", lambda x: message_label.config(text = ""))

    root.mainloop()

if __name__ == "__main__":
    tkmain()