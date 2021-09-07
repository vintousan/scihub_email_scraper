#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Email scraper
# Author: VJA
# Description: Get email in papers (PDF format) downloaded from SciHub using csv of email files. 
# Tech: Beautiful Soup (Data scraper from http and xml files), PyPDF2 (Data scraper from PDF files)

# Notes: 
# 1 - Some papers downloaded from Scihub are incorrect. Use with caution. 
# 2 - Scihub may detect unusual traffic. The code may work after some time


# In[1]:


# Import libraries
import os
from bs4 import BeautifulSoup as bs  # noqa: E402
import requests  # noqa: E402
import csv
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
import random
import time
import random


# In[7]:


# Get scihub website
#scihub = 'https://sci-hub.do/'
scihub = 'https://sci-hub.se/'


# In[3]:


# List DOI strings from csv
doi_str = []

with open('C:\\Users\\ERDT\\Desktop\\doi_tencon2019.csv') as file: # Read CSV file
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        substring = '10.' # Filter: DOI usually starts with a number. 
        if substring in row[0]:
            # Get DOI
            doi_str.append(row[0])


# In[4]:


for doi in doi_str[102:]:
    print(doi)


# In[5]:


# Define file path of downloaded PDFs
file_path = 'C:\\Users\\ERDT\\Desktop\\tencon2019_first_pages\\'
if not os.path.exists(file_path):
    os.mkdir(file_path)


# In[14]:


# Version 1
file_count = 1

for doi in doi_str[102:]:
    
    if(file_count % 10 == 0):
        random_wait_time = random.randint(60,120) #Waiting between 2 - 3 mins 
        print('Sleeping at {} s...'.format(random_wait_time))
        time.sleep(random_wait_time)
    
    # Access URL
    url = scihub + doi
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    
    # Get download mirror
    mirror = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
    if mirror.startswith('//'):
        mirror = mirror[2:]
        mirror = 'https://' + mirror
    
    # Access PDF from download mirror
    pdf_str = '.pdf'
    if pdf_str in mirror:
        response_mirror = requests.get(mirror)
        with io.BytesIO(response_mirror.content) as f:
            pdf_reader = PdfFileReader(f)
            pdf_writer = PdfFileWriter()
            page_num = 0
            pdf_writer.addPage(pdf_reader.getPage(page_num))
            
            # Generate valid filename for downloaded PDF
            substr_1 = '/'
            substr_2 = '_'
            doi_edited = doi.replace(substr_1, substr_2)
            output_filename = '{:02d}'.format(file_count) + file_path + '{}_page_1.pdf'.format(doi_edited)
            
            with open(output_filename,'wb') as out:
                pdf_writer.write(out)
                
    file_count += 1


# In[8]:


# Version 2
file_count = 145

for doi in doi_str[144:]:
    
    if(file_count % 10 == 0):
        random_wait_time = random.randint(60,120) #Waiting between 2 - 3 mins 
        print('Sleeping at {} s...'.format(random_wait_time))
        time.sleep(random_wait_time)
    
    # Access URL
    url = scihub + doi
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    
    # Get download mirror
    btn = soup.find("button")
    btn_text = btn.text
    btn_onclick = btn['onclick']
    mirror = btn_onclick[15:-1]
    
    #mirror = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
    if mirror.startswith('//'):
        mirror = mirror[2:]
        mirror = 'https://' + mirror
    
    # Access PDF from download mirror
    pdf_str = '.pdf'
    if pdf_str in mirror:
        response_mirror = requests.get(mirror)
        with io.BytesIO(response_mirror.content) as f:
            pdf_reader = PdfFileReader(f)
            pdf_writer = PdfFileWriter()
            page_num = 0
            pdf_writer.addPage(pdf_reader.getPage(page_num))
            
            # Generate valid filename for downloaded PDF
            substr_1 = '/'
            substr_2 = '_'
            doi_edited = doi.replace(substr_1, substr_2)
            output_filename = file_path + '{:03d}_'.format(file_count) + '{}_page_1.pdf'.format(doi_edited)
            
            with open(output_filename,'wb') as out:
                pdf_writer.write(out)
                
    file_count += 1


# In[9]:


# List downloaded PDFs
filename_list = [f for f in os.listdir(file_path) if f.endswith('.pdf')]


# In[6]:


search_str = []

for doi in doi_str:
    search_str.append(doi[8:])


# In[21]:


count = 1

for search in search_str:
    
    for file_name in filename_list:
        if search in file_name:
            file_name_temp = file_name
            break
   
    f = file_path + file_name_temp
    new_file_name = file_path + str(count) + '_' + file_name_temp
    os.rename(f, new_file_name)
    count += 1


# In[20]:


print(file_name_temp)


# In[9]:


for file_name in filename_list:
    f = file_path + file_name
    os.rename(f, (file_path + file_name[2:]))


# In[10]:


for i in filename_list:
    print(i)


# In[18]:


for i in search_str:
    print(i)


# In[13]:


contacts = []

abstract = 'Abstract'
email_sign = '@'

count = 103

for file in filename_list:
    
    print(count)
    
    f = file_path + file
    pdf_reader = PdfFileReader(f)
    
    numpage = 0
    page = pdf_reader.getPage(numpage)
    page_content = page.extractText()
    
    if abstract in page_content:
        end_of_contacts = page_content.index(abstract)
        contact_temp = page_content[:end_of_contacts]
        hello = contact_temp.split('\n')
        
        for line in hello:
            if email_sign in line:
                print(line)
                
    count += 1

