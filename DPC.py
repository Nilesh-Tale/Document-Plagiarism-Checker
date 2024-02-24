from email.mime import base
import os
import gridfs

from pymongo import MongoClient

from xml.dom.minidom import Element
import PySimpleGUI as sg


from pydoc import doc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from googletrans import Translator

import PyPDF2


from deep_translator import GoogleTranslator






###########################################################################################3


theme_dict = {'BACKGROUND': '#FFFFFF',
                'TEXT': '#000000',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}


# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

BORDER_COLOR = '#B2BEB5'
DARK_HEADER_COLOR = '#FFFFFF'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))

top_banner = [[sg.Text('Document Plagiarism Checker', font='Any 20', background_color=DARK_HEADER_COLOR),
               sg.Text('Group No. 15', font='Any 15', background_color=DARK_HEADER_COLOR)]]
"""
top_banner = [[sg.Text('Document Plagiarism Checker', font='Any 20'),
               sg.Text('Group No. 15', font='Any 15' )]]
"""




block = [[sg.Text('DashBoard', font='Any 20')],
            
            [sg.Text("Upload Files Here: ")],
            [sg.Text("_"*120)],
            [sg.Text(" ")],
            [sg.Text(" ")],
            [sg.Text(" "*70), sg.Button("UPLOAD", font = 25)],
            [sg.Text(" ")],
            
            [sg.Text(" "*65),sg.Button('LogOut', font=25),sg.VSeparator(),sg.Button('Exit', font=25)]
            ]
 

layout = [[sg.Column(top_banner, size=(800, 60), pad=(20, 20))],
          [sg.Column(block, vertical_alignment='center', justification='center',size=(800,400),  pad=(20,20), k='-C-')]]


###########################################################################################3


# fold=[]

###########################################################################################3


#Upload files
def uploadfiles(file, filename):
        print("______________________________")    
        
        print("")
        print(file)
        print("")
        
        print("_____________________________________")
        
        file_location=file
        file_data=open(file_location,"rb")
        data=file_data.read() 
        fs=gridfs.GridFS(db)
        fs.put(data, filename=filename)
        print("Upload complete file") 
        
        data=db.fs.files.find_one({'filename':filename})
        my_id=data['_id']
        outputdata=fs.get(my_id).read()
        download_location="E:\\BE\\BE\\BERT-DPC\\Uploaded_files\\"+filename
        output=open(download_location,"wb")
        output.write(outputdata)
        output.close()
        print("Download file complete")
        


###########################################################################################3

        
#Mongo Connection
def mongo_conn():
    try:
        conn = MongoClient(host = "mongodb://localhost:27017/")
        print("MongoDB connected", conn)
        return conn.grid_file
    except Exception as e:
        print("Error in mongo connection:", e)
        
db=mongo_conn()




###########################################################################################3

#Bert Algorithm

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('bert-base-nli-mean-tokens')
model.max_seq_length = 512

# Two lists of sentences
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('bert-base-nli-mean-tokens')


from nltk.tokenize import sent_tokenize


def Bert(fname):
    
    list=[]

       
    for file in fname:
                
                split_fname=os.path.splitext(basefilename)
                # print(split_fname)
                file_extension=split_fname[1]
                
                translated = GoogleTranslator(source='auto', target='english').translate_file(file)
                list.append(translated)
    
    
    print(list)
                    
    doc1= sent_tokenize(list[0])
    doc2= sent_tokenize(list[1])
    
    # print(doc1)
    # print(doc2)
    
    #Compute embedding for both lists
    embeddings1 = model.encode(doc1, convert_to_tensor=True)
    embeddings2 = model.encode(doc2, convert_to_tensor=True)
    
    
    
    ###########################################################################################3

    #Compute cosine-similarits
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    
    score_list=[]
    
    if(len(doc1)>len(doc2)):
        for i in range(len(doc2)):
            print("{:.4f}".format(cosine_scores[i][i]))
            score_list.append(float(cosine_scores[i][i]))
    
    elif(len(doc2)>len(doc1)):
        for i in range(len(doc1)):
            print("{:.4f}".format(cosine_scores[i][i]))
            score_list.append(float(cosine_scores[i][i]))
    
    print(score_list)
    
    try:
        avg=float(sum(score_list)/len(score_list))
    
    except:
        avg=1
    
    print("Documents Similarity Percentage is {:.4f}".format(avg*100))
    
    Pie(avg)
###########################################################################################3
    
    
    
    
########################################################################################################
#Ploting PieChart

def Pie(output):
    plagiarised=output*100

    # Data to plot
    labels = 'Plagiarised', 'Non-Plagiarised'

    nonPlagiarised=100-plagiarised

    sizes = [plagiarised, nonPlagiarised]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()
    
###########################################################################################3




###########################################################################################3

window = sg.Window('Document Plagiarism Checker', layout,  background_color=BORDER_COLOR,  grab_anywhere=True)
"""
window = sg.Window('Document Plagiarism Checker', layout,  grab_anywhere=True)
"""

while True:             # Event Loop
    event, values = window.read()
    
    if event == "UPLOAD":
        
        fname, check = sg.Window('Window Title').Layout([[sg.Input(key='_FILES_'), sg.FilesBrowse()], [sg.OK(), sg.Cancel()]]).Read()
        fname=check["_FILES_"].split(';')
        print(fname)   
        
        if check:
            
            for file in fname:
                basefilename=os.path.basename(file)
                uploadfiles(file,basefilename)
            
            sg.popup_timed("Files Uploaded Sucessfully!")
            Bert(fname)
            
        
        

        #sg.Popup.close()
        #sg.PopupAutoClose()
       
      
    if event == 'LogOut':
        window.close()
        os.system('python Login.py')
        
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()


###########################################################################################3
