from pdf_util import PDFUtility
import PySimpleGUI as sg
import os
import random
from pdf_util import color_dict

def bookMarkAdderMain(input_file_path, output_folder_path,search_strings):
    input_file = input_file_path

    # construct output file path based the folder path
    output_file = os.path.join(output_folder_path,os.path.basename(input_file))

    # print(search_strings)

    #should read this from the file
    # search_texts = [" O.C. ", " Shear Wall ", " On-center ", " Panel ", " Roof ", " Low Eave ", " Parapet " , " Bump-out "]

    search_texts = [sublist[0] for sublist in search_strings]

    search_text_colors = [sublist[1] for sublist in search_strings]

    pdf_bookmark_adder = PDFUtility(input_file, output_file)

    # loop through the search text and call bookmark adder function on each of the search string
    for i in range(len(search_texts)):
        pdf_bookmark_adder.add_bookmarks_from_text(search_texts[i],color_dict[search_text_colors[i]])
    pdf_bookmark_adder.save_pdf_file()

def bookMarkAdderBulk(input_file_paths, output_folder_path,search_strings):
    
    #iterate through all the input file path locations
    for input_file_path in input_file_paths:

        # call the main function which generate the bookmarked pdf
        bookMarkAdderMain(input_file_path,output_folder_path,search_strings)


# Define the layout of the window
layout = [
    [sg.Text('Select PDF files:', size=(15, 1)), sg.Input(key='-FILES-', enable_events=True, visible=False), sg.FilesBrowse(file_types=(("PDFFiles", "*.pdf"),))],
    [sg.Listbox(values=[], key='-FILELIST-', size=(70, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
    [sg.Text('Select Output Folder:', size=(15, 1)), sg.Input(key='-FOLDER-', enable_events=True, disabled=True), sg.FolderBrowse('Browse')],
    [sg.Button('Process Files'), sg.Button('Remove')]
]

secondLayout = [
    [sg.Text('Select Text File:', size=(13, 1)),sg.Input(key='-TEXTFILES-', enable_events=True, visible=False), sg.FilesBrowse(file_types=(("TextFiles", "*.txt"),))],
    [sg.Text('Select Color:', size=(10, 1)), sg.Combo(values=list(color_dict.keys()), key='-COLOR-', enable_events=True),sg.Button('Set Color')],
    [sg.Listbox(values=[], key='-SEARCHLIST-', size=(70, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
]

# ----- Full layout -----
mainlayout = [
    [sg.Column(layout),
     sg.VSeperator(),
     sg.Column(secondLayout),]
]

# window = sg.theme('SolarizedLight')
# Create the window
window = sg.Window('PDF Utility', mainlayout)

selected_files = []

output_folder = ''

search_strings = []

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == '-FILES-':
        # Update the input field with selected files
        #window['-FILES-'].update(value=values['-FILES-'])

        # Get the list of selected files
        temp_files = values['-FILES-'].split(';')
        selected_files.extend(temp_files)

        # remove duplicates
        selected_files = list(set(selected_files))

        # Update the file listbox
        window['-FILELIST-'].update(values=selected_files)

    if event == 'Process Files':

        #check if the list is empty
        if not selected_files or len(output_folder) == 0:
            sg.popup_error('No files are selected. Need to add atlease one file to start processing them', title='Empty Selection')
        elif len(search_strings) == 0:
            sg.popup_error('No search strings are present', title = "Empty Search String")
        else:
            # Process all the files in the list box
            bookMarkAdderBulk(selected_files,output_folder,search_strings)
        
        print(f'Process completed')

    if event == 'Remove':
        # fetch the selected file list
        selected_files_from_list = values['-FILELIST-']

        # remove the selected options from the global selected files array
        selected_files = list(filter(lambda x: x not in selected_files_from_list, selected_files))

        # remove the selected options from the listbox 
        window['-FILELIST-'].update(values=selected_files)
    
    if event == '-FOLDER-':
        output_folder = values['-FOLDER-']
    
    if event == '-TEXTFILES-':
        text_file_location = values['-TEXTFILES-']
        lines = []
        with open(text_file_location, 'r') as file:
            lines = []
            for line in file:
                # Remove trailing newline character
                line = line.rstrip('\n')
                lines.append(line)
            temp_strings = [' ' + string + ' ' for string in lines]
            search_strings.clear
            for string in temp_strings:
                search_strings.append([string,random.choice(list(color_dict.keys()))])

            window['-SEARCHLIST-'].update(values=search_strings)
    
    if event == 'Set Color':
        # print (search_strings)
        selected_search_string = values['-SEARCHLIST-']

        selected_color = values['-COLOR-']

        for i in range(len(search_strings)):
            if (len(selected_search_string) == 1) and (search_strings[i] == selected_search_string[0]) and (len(selected_color) > 0):
                search_strings[i][1] = selected_color
        
        window['-SEARCHLIST-'].update(values=search_strings)
        # print(selected_search_string)



      

# Close the window
window.close()