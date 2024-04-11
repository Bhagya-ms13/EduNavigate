import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
    return text

def split_text_by_headings(text):
    # Split the text into sections based on headings
    sections = re.split(r'\n[A-Z\s]+\n', text)
    return sections

def summarize_sections(sections, num_sentences=3):
    summarizer = LsaSummarizer()
    summaries = []
    for section in sections:
        parser = PlaintextParser.from_string(section, Tokenizer("english"))
        summary = summarizer(parser.document, num_sentences)
        summary_text = " ".join([str(sentence) for sentence in summary])
        summaries.append(summary_text)
    return summaries

def summarize_pdf(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    sections = split_text_by_headings(pdf_text)
    summaries = summarize_sections(sections)
    return summaries

def summarize_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            summaries = summarize_pdf(file_path)
            messagebox.showinfo("Summarized Text", "\n\n".join(summaries))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the Tkinter window
window = tk.Tk()
window.title("PDF Summarizer")

# Load and set background image
bg_image = PhotoImage(file=r"C:\Users\jjoan\Downloads\png-transparent-children-on-books-illustration-icon-books-child-comic-book-reading-thumbnail.png")
bg_image = bg_image.zoom(2, 2)  # Increase size by a factor of 2
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Add a button with customized size, font color, and background color
summarize_button = tk.Button(window, text="Summarize PDF", command=summarize_button_click, font=("Arial", 30), fg="white", bg="crimson", width=20, height=2)
summarize_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Run the Tkinter event loop
window.mainloop()
