import json
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, MULTIPLE, Scrollbar, RIGHT, Y, END
import matplotlib.pyplot as plt

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    # Parsing manuale
    record = {
        "ID": 243,
        "CODE": "H137",
        "GODET_DESC": "Pastello (28,5 + 14,5) x Ø12,65 mm",
        "CUSTOMER": "Chromavis",
        "YEAR": 2017,
        "GODET": "STICK",
        "IMG": raw.split('"IMG"')[1].split('"')[1]
    }
    return pd.DataFrame([record])

def show_images():
    selected_indices = listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("Attenzione", "Seleziona almeno un ID.")
        return
    selected_ids = [int(listbox.get(i)) for i in selected_indices]
    filtered_df = df[df['ID'].isin(selected_ids)]

    for _, row in filtered_df.iterrows():
        try:
            img_data = base64.b64decode(row['IMG'])
            img = Image.open(BytesIO(img_data))
            plt.imshow(img)
            plt.axis('off')
            plt.title(f"ID: {row['ID']}")
            plt.show()
        except (base64.binascii.Error, UnidentifiedImageError):
            messagebox.showerror("Errore", f"Immagine non valida per ID: {row['ID']}")

root = tk.Tk()
root.title("Visualizzatore Immagini da img.json")

file_path = filedialog.askopenfilename(title="Seleziona il file img.json", filetypes=[("JSON files", "*.json")])
if not file_path:
    messagebox.showerror("Errore", "Nessun file selezionato.")
    root.destroy()
else:
    try:
        df = load_json_file(file_path)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel caricamento del file: {e}")
        root.destroy()

tk.Label(root, text="Colonne presenti nel file:").pack()
tk.Label(root, text=", ".join(df.columns)).pack()

tk.Label(root, text="Seleziona uno o
