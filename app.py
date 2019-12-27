# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:58:50 2019

@author: amaurya
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from unidecode import unidecode
from googletrans import Translator
import time
from datetime import date
import timeit
import base64
import datetime
st.title('Projects')

def main():
    # Render the readme as markdown using st.markdown.
    #readme_text = st.markdown(get_file_content_as_string("instructions.md"))
    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Local Language Translation", "Show instructions"])

    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Local Language Translation".')
    elif app_mode == "Local Language Translation":
        #readme_text.empty()
        st.sidebar.success('To get instruction select a radio box from below.')
        st.title("Local Language Translation")
        translation()




def file_chooser():
    file_bytes = st.file_uploader("Upload a file", type=("xlsx"))    
    if file_bytes is not None:
        with st.spinner('Wait for it...'):
            data = pd.read_excel(file_bytes)
            st.success('File uploaded succesful!!')
        #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
        #st.write('You selected `%s`' % filename)
    else:
        data=pd.DataFrame()
        #st.error('Unable to Load the selected file.Please choose another!!')
    return data
 
def show_language_inst():
    st.write("first upload the file usign the file chooser")


def translation():
    #data=download_fi()
    #filename = file_selector()
    #st.write('You selected `%s`' % filename)
    if st.sidebar.checkbox("Show Intruction"):
        show_language_inst()
    else:
        st.write("Choose a File")
        data=file_chooser()
        st.subheader("Source Data")
        if st.checkbox("Show Source Data"):
            st.write("The Sample Data is as follows:")
            st.write(data.head())
        if st.checkbox("Show list of Columns"):
            st.write("The columns are:")
            #abc=data.columns
            st.write(data.columns)
        msg1=("Total number of records to be translated : " + str(len(data)))
        st.info(msg1)
        cols_for_translation = st.multiselect('Select columns to be tranlsated', data.columns)
        newdf=pd.DataFrame(data[cols_for_translation])
        #newdf=pd.DataFrame(data)
        if st.checkbox("Show selected Columns data"):
            #space=st.empty()
            if cols_for_translation is not None:
                st.markdown("> *These columns will be used for Translation*")
                st.table(newdf.head())
                    #st.write(newdf.head())"""
        #new_df = data[[]]
        #st.write(new_df)
        #st.subheader("Enter output filename or by default Standard name will be given:")
        #output_name= st.text_input(" ")
        if st.button("Start Webscraping"):
            with st.spinner('Processing File...'):
                out=startWebscraping(data,cols_for_translation)
                st.success('Completed! **You can download the file using the below Link :)**')
            st.balloons()
            #if output_name is not None:
            #    csv = out.to_csv(index=False)
                #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
            #else:
            #    output_name="Default"
            #    csv = out.to_csv(index=False)
                #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
            csv = out.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}">Download Output File</a> (right-click and save as &lt;some_name&gt;.csv)'
            st.markdown(href, unsafe_allow_html=True)
                #output_name=("Output_",datetime.datetime.today())
        else:
            st.markdown("> ** Click on Start webscraping Button to Start the processing ** ")
        
        #with st.echo():
        #    st.write('This code will be printed')
        #st.write('The current movie title is', title)
            
  
def startWebscraping(excel,cols_for_translation):
    excel.fillna(" ",inplace=True)
    data_std=pd.DataFrame(excel)
    #col_to_check_trans=get_col_list()
    conditionals=checklist(data_std,cols_for_translation)
    print("Displaying Sample Record...")
    print(data_std.iloc[1])
    
    a=None
    for i in range(len(conditionals)):
        if i==0:
            a=conditionals[i]
        elif i<(len(conditionals)):
            a=(a&conditionals[i])
    print(a.value_counts())
    
    print("--------------------Starting Translation-----------------------")
    
    to_be_translated=data_std[a==False]
    
    translated=get_translation(to_be_translated,cols_for_translation)
    
    dictOfWords = { i : cols_for_translation[i] for i in range(len(cols_for_translation) ) }
    ready_translated_data=pd.DataFrame(translated).transpose().rename(columns=dictOfWords)
    for col in cols_for_translation:
        to_be_translated[col]=ready_translated_data[col].to_list()
    
    output=data_std[a==True].append(to_be_translated)
    return output
    #output.to_excel(output_file_path+"\\Output_"+str(date.today())+"_"+out_name,index=False)
    
def standard_changes(data_csv,data_excel):
    new_data_csv=[]
    new_data_excel=[]
    if len(data_csv)>0:
        for csv in data_csv:
            csv.fillna(" ",inplace=True)
            specific_data=pd.DataFrame(csv)
            new_data_csv.append(specific_data)
    if len(data_excel)>0:
        for excel in data_excel:
            excel.fillna(" ",inplace=True)
            specific_data=pd.DataFrame(excel)
            new_data_excel.append(specific_data)
    if len(new_data_csv)>0 and len(new_data_excel)>0:
        return new_data_csv,new_data_excel
    elif len(new_data_csv)==0 and len(new_data_excel)>0:
        return new_data_excel[0]
    else:
        return new_data_csv[0]
    
def get_true(test_string):
    condition_val=None
    for string in list(test_string):
        flag=0
        if ord(string)< 32 or ord(string)>126:
            flag=1
            break
        else:
            flag=0
            continue
    if flag==1:
        condition_val=False
    else:
        condition_val=True
    return condition_val

def checklist(data,columns):
    list_conditions=[]
    for i in range(len(columns)):
        current_columns=columns[i]
        values_true_false=data[current_columns].apply(get_true)
        list_conditions.append(values_true_false)
    return list_conditions


def get_translation(data,col_to_check_trans):
    translator = Translator()
    cols=[]
    count = 1
    print("Columns checked for translation:")
    for i in col_to_check_trans:
    	print("--->",i)
    for i in col_to_check_trans:
        values_to_translate=data[i].tolist()
        col_values=[]
        start = timeit.default_timer()
        for j in values_to_translate:
            j=j.replace('ß', 'ss').replace('￤', ' ').replace('|', ' ').replace('-',' ').replace('[',' ').replace(']',' ').replace('?',' ').replace('￟',' ')
            translated_google=translator.translate(j, dest='en')
            translated_google=unidecode(translated_google.text)
            col_values.append(translated_google)
            time.sleep(1)
            if count == 5:
             	time_prec = timeit.default_timer()
             	expected_time = np.round((time_prec - start) / (count / len(values_to_translate)) / 60, 2)
             	print('---------------------------------->Expected Time To Complete:', expected_time, 'minutes')
            if count == 5:
                time_prec = timeit.default_timer()
                expected_time=np.round((time_prec-start)/(count/len(values_to_translate))/60,2)
                msg1=("Expected time: "+str(expected_time)+' minutes')
                st.info(msg1)
            print(translated_google)
            count+=1
        cols.append(col_values)
    return cols   

if __name__ == "__main__":
    main()
