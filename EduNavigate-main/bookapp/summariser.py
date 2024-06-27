#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/Saifullah3711/text_summarizer_hugging_face/blob/main/text_summarization_huggingface_transformer.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Installing the Dependencies

# In[1]:





# # Importing Dependencies

# In[2]:


from transformers import pipeline
import PyPDF2
from pdfminer.high_level import extract_text
import resource
import re
import textwrap
from fpdf import FPDF
from django.conf import settings
import os
# In[3]:


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# # Individual Functions for summarization

# In[4]:


# This function tweak the text before saving in the pdf
def prep_b4_save(text):
  text = re.sub('Gods', 'God\'s', text)
  text = re.sub('yours', 'your\'s', text)
  text = re.sub('dont', 'don\'t', text)
  text = re.sub('doesnt', 'doesn\'t', text)
  text = re.sub('isnt', 'isn\'t', text)
  text = re.sub('havent', 'haven\'t', text)
  text = re.sub('hasnt', 'hasn\'t', text)
  text = re.sub('wouldnt', 'wouldn\'t', text)
  text = re.sub('theyre', 'they\'re', text)
  text = re.sub('youve', 'you\'ve', text)
  text = re.sub('arent', 'aren\'t', text)
  text = re.sub('youre', 'you\'re', text)
  text = re.sub('cant', 'can\'t', text)
  text = re.sub('whore', 'who\'re', text)
  text = re.sub('whos', 'who\'s', text)
  text = re.sub('whatre', 'what\'re', text)
  text = re.sub('whats', 'what\'s', text)
  text = re.sub('hadnt', 'hadn\'t', text)
  text = re.sub('didnt', 'didn\'t', text)
  text = re.sub('couldnt', 'couldn\'t', text)
  text = re.sub('theyll', 'they\'ll', text)
  text = re.sub('youd', 'you\'d', text)
  return text


# In[5]:


# This function convert the text into the pdf and save it at the specified location
def text_to_pdf(text, filename):
    a4_width_mm = 200
    pt_to_mm = 0.35
    fontsize_pt = 11
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')
    print("PDF of summary Saved!!")


# In[6]:


# This function split a huge corpus of text into small chunks or portions
def text_chunking(new_text):
  max_chunk = 500
  new_text = new_text.replace('.', '.<eos>')
  new_text = new_text.replace('?', '?<eos>')
  new_text = new_text.replace('!', '!<eos>')

  sentences = new_text.split('<eos>')
  current_chunk = 0 
  chunks = []
  for sentence in sentences:
      if len(chunks) == current_chunk + 1: 
          if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
              chunks[current_chunk].extend(sentence.split(' '))
          else:
              current_chunk += 1
              chunks.append(sentence.split(' '))
      else:
          # print(current_chunk)
          chunks.append(sentence.split(' '))

  for chunk_id in range(len(chunks)):
    chunks[chunk_id] = ' '.join(chunks[chunk_id])
  print("Total chunks of text are: ", len(chunks))
  return chunks


# In[7]:


# This function takes in all the chunks, find the summary of each chunk and return all the summaries of chunks in list form. 
def model_summary(chunks):
  print("Summarizing the text. Please wait .......")
  all_summaries = []
  count = 0
  for chunk in chunks:
    print("Summarizing Chunk NO: ", count + 1)
    res = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
    all_summaries +=res
    count +=1
  return all_summaries


# # Combining all the individual parts into a single function
# * Input to this function is path to the pdf
# * This function do all the pre-processing, get the summary and save it in the pdf
# * Parameter to this function is only the path to the pdf

def find_summary(pdf_path):
  raw_text = extract_text(pdf_path)  # Extract text from the path of pdf given
  chunks = text_chunking(raw_text)   # chunk the large text into small parts so it can be supplied to the model
  all_summaries = model_summary(chunks) # passing the chunks to the model for the summarization
  joined_summary = '\n'.join([summ['summary_text'] for summ in all_summaries])  # combine all chunks of summaries to single
  txt_to_save = (joined_summary.encode('latin1','ignore')).decode("latin1")  # This ignore the "aphostrope" which is little problematic
  txt_to_save_prep = prep_b4_save(txt_to_save)
  spl = pdf_path.split('/') # Splitting the path based on "/" to get the name of the book or pdf
  file_name = spl[-1][:-4]+"_summary.pdf" # Summary is added at the end i.e book name is the_alchemist so it becomes -> the_alchemist_summary.pdf etc. 
  pdf_path = os.path.join(settings.MEDIA_ROOT,'pdf',file_name.lstrip('/'))
  print(pdf_path)
  text_to_pdf(txt_to_save_prep, pdf_path)
  return pdf_path
# pdf_path_forty = "/Users/indulekhaag/Downloads/Django-Book-WebSite-main/media/pdf/1.pdf"
# find_summary(pdf_path_forty)





