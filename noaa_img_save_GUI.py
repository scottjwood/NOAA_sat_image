from urllib.request import urlopen
from urllib.error import URLError # Not implemented yet, need to import 404 error proofing
from bs4 import BeautifulSoup
import os
import time
import re
from tkinter import *
from tkinter import filedialog
from sys import stdout # this is for the console printer to repeat

#### Live Data
url = 'http://www.aviationweather.gov/adds/data/satellite/'
get_thumbnails = False # get small or large images
timedelay = 60 * 60 # how long until getting next images
run_how_many_times = 1 # 

area = ['AK', 'COD', 'DEN', 'CARIB', 'GULF']
imgtype = ['_ir.jpg', '_irbw.jpg', '_vis.jpg', '_wv.jpg']

####### Timer tool - yet to be determined if I'll use it #####
def scott_printer(myimg, countleft):
    """My console printer"""
    stdout.write("\rCurrent Image: %s | %d images left" % (myimg, countleft))
    stdout.flush()

def filewriter(the_dir, myfilename):
    '''Writes file to disk'''
    my_path = the_dir + '/' + myfilename
    d = os.path.dirname(my_path)
    if not os.path.exists(d):
        os.makedirs(d)
    f = open(my_path,'wb')   # create new file locally
    f.write(urlopen(url + myfilename).read()) # Open remote file, write to newly created file
    f.close() # close file from memory

def find_and_write(selected_list, the_dir):
    '''Find my images on a page'''
    noaa_sat = urlopen(url) # retrieve page
    html = noaa_sat.read() # make page readable
    page = html.decode("utf8") # not sure if this is really needed, but decode to utf8
    soup_var = BeautifulSoup(page) # create soup list
    # Define Search Patterns
    if get_thumbnails: # get small images
        # pattern = re.compile(r'' + area + imgtype)
        pattern = re.compile('|'.join(selected_list))
    else: # get large images
        #pattern = re.compile(r'(?<!sm_)' + area + imgtype)
        pattern = re.compile('|(?<!sm_)'.join(selected_list))
    
    anchor_tags = soup_var.findAll('a', text=pattern) # find all relevant <a> tags
    existing_files = os.listdir(the_dir) # check existing files
    anchor_strings = []
    for a_tag in anchor_tags: # make <a> tags into strings
        anchor_strings.append(a_tag.contents[0].string)
    new_files = [file for file in anchor_strings if not file in existing_files]
    # check files vs. what already exists in folder, 
    # create new_files list from that list, converting soup to strings at the same time

    # remove the file containing 'latest' since it exists
    if len(new_files) > 0: 
        if 'latest' in new_files[-1]: new_files.pop() 
    else: pass
    # console counter variable / non-critical
    count = len(new_files)
    total = len(anchor_tags)
    print("%s Total Files | %s New Files" % (str(total), str(count))) # tell me in console how many new images

    # loop through all new image names
    for img in new_files: 
        count -= 1 # console counter
        filewriter(the_dir, img) # run filewriter function
        scott_printer(img, count)
        # print(img) # tell me what the shitshow is going on in console.
        # print(str(count) + " images left") # console counter


######### Tkinter GUI #################################################################
class NOAA_sat_app(Frame):
    def __init__(self, master=None):
        self.root = master
        self.createWidgets()

    def run_satellite_function(the_dir, areas, imgtypes):
        '''Run the the entire scrape and print results'''
        mycount = run_how_many_times
        for gather_imgs in range(run_how_many_times):
            mycount -= 1
            print("Running")
            selected_items_list=merge_options(areas, imgtypes)
            find_and_write(selected_items_list, the_dir) # run function with specific type
            # Finished with current time, log and wait
            timestamp = time.localtime()
            print("\n\n-------------------------------")
            print("---Images Downloaded ----------\n-------------------------------")
            if run_how_many_times > 1: # check if run more than once
                time.sleep(timedelay) # Sleep for time interval
    
    def createWidgets(self):
        """ Create widgets inside Window
        """
        ########### Main Window Properties #####
        # self.iconbitmap(default="")  # add ico file here, replaces default red icon
        self.root.geometry("540x500")
        self.root.title("NOAA Satellite Download App")
        self.root.attributes("-alpha", 1.0)
        #self.root.protocol("DELETE_my_root", master.destroy())

        #### Images in Base64 ########
        self.program_title_gif = PhotoImage(format='gif', data="R0lGODlh9AF9AMQCAKurq8LCwu3t7bu7u7Kysi0tLfz8/Nra2uXl5enp6YeHh97e3vr6+uLi4mVlZfb29kZGRs3NzcjIyFNTU3Z2dpqamvf39/Dw8NXV1dHR0ZKSkqKiohUVFfPz8wAAAP///yH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS4zLWMwMTEgNjYuMTQ1NjYxLCAyMDEyLzAyLzA2LTE0OjU2OjI3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M2IChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDoxNTVDMkM2OTMxM0UxMUUyQURFNEVGMEUyRDEzN0MzOCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoxNTVDMkM2QTMxM0UxMUUyQURFNEVGMEUyRDEzN0MzOCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjE1NUMyQzY3MzEzRTExRTJBREU0RUYwRTJEMTM3QzM4IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjE1NUMyQzY4MzEzRTExRTJBREU0RUYwRTJEMTM3QzM4Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJy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")
        self.open_img = PhotoImage(format='gif', data="R0lGODlhEAAQAIcAADFKY0L/QplnAZpoApxqBJ5sBqBuCKJwCqNxC6RyDKVzDad1D6x6FLB+GLOBG7WCHbeEH7qHIr2KJcaaGcaaGsKPKsiVMMmWMcuYM8yZNMmgIc+iJte4QNq/bOKzQ+LBUP3VcP/bdfDkev/kf5SlvZylvbe3t5ytxqW11qm92r3GxrnK5P/XhP/rhP/viffwif/4k///mf//nP//pcTExMXFxc3NzdHR0cbW69jh8efv9+vz//r7/P///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAMAAAEALAAAAAAQABAAAAiZAAMIHEiwoMGDBzNkwHDBAkKBGXpI5MGjAsKIMjJm7CEhAoQHDhoIxNBDo0mJEhncCHChB4yXMGPKWFBjgs2bOG1+aIGAxoQYJk3G6DCBhQGfQGPClPFiAogCNAL8dEG1KtUZGjwQiPpTxoivYEfM4LBhQFSpMUKoXatWBAUBNQROUECXboIDBgoQGGDCxkAbNAILHuz34cGAADs=")
        
        # Define text styles
        title_padding = 30
        title_fonts = ("Helvetica", 18)

        ############### main frame ##############
        self.fFrame = Frame(self.root, padx=5, pady=15)
        self.fFrame.pack()
        tool_title = Label(self.fFrame, text='NOAA Satellite Image Tool', image=self.program_title_gif)
        tool_title.pack(side=LEFT)
        self.frame_settings = Frame(self.root, padx=0)
        self.frame_settings.pack()

        #### Location Settings
        setting_location = Label(self.frame_settings, text='LOCATION', padx=title_padding, font=(title_fonts))
        setting_location.grid(row=0, column=0)

        #### Location Listbox
        frame_location = Frame(self.frame_settings, padx=5, pady=5)
        frame_location.grid(row=1, column=0)

        scrollBar_loc = Scrollbar(frame_location)
        scrollBar_loc.pack(side=RIGHT, fill=Y)
        frame_location.listBox = Listbox(frame_location, selectmode=EXTENDED , exportselection=0, width=35)
        frame_location.listBox.pack(side=LEFT, fill=Y)
        scrollBar_loc.config(command=frame_location.listBox.yview)
        frame_location.listBox.config(yscrollcommand=scrollBar_loc.set)
        area.sort()
        for place in area:
            frame_location.listBox.insert(END, place)
        frame_location.listBox.select_set(2) # Set Default selection

        #### Image Type Settings
        setting_imgtype = Label(self.frame_settings, text='IMAGE TYPES', padx=title_padding, font=(title_fonts))
        setting_imgtype.grid(row=0, column=1)

        #### Location Listbox
        frame_imgtype = Frame(self.frame_settings, padx=5, pady=5)
        frame_imgtype.grid(row=1, column=1)

        frame_imgtype.listBox = Listbox(frame_imgtype, selectmode=EXTENDED , exportselection=0, width=35)
        frame_imgtype.listBox.pack(side=LEFT, fill=Y)
        imgtype.sort()
        for place in imgtype:
            frame_imgtype.listBox.insert(END, place)
        frame_imgtype.listBox.select_set(0) # Set Default selection

        #### Start File browser button
        frame_directory = Frame(self.frame_settings)
        self.svDir = StringVar(value='C:/') # Directory string for button     
        frame_directory.grid(row=2, column=0, pady=5)
        print("self.svDir is this: %s" % self.svDir.get())

        frame_directory.run_button = Button(self.frame_settings, image=self.open_img, width=20, pady=20, command = self.load_dir)
        frame_directory.run_button.grid(row=3, column=0, sticky=W)
        
        self.eDir = Entry(self.frame_settings, width=30, textvariable=self.svDir)
        self.eDir.grid(row=4, column=0)

        #### Run Button
        frame_run_button = Frame(self.frame_settings)
        frame_run_button.grid(row=2, column=1, pady=5)
        def check_selected_options():
            # areas = frame_location.listBox.curselection()
            # areas = [area.[int(item)] for item in areas]
            # imgtypes = frame_imgtype.listBox.curselection()
            # imgtypes = [imgtype[int(item)] for item in imgtypes]
            # return areas, imgtypes

        frame_run_button.run_button = Button(self.frame_settings, text='Run!', bg="LightSkyBlue", width=10, pady=10, command=lambda : run_satellite_function(self.svDir.get(), check_selected_options()))
        frame_run_button.run_button.grid(row=3, column=1, sticky=E)

    def load_dir(self):
        '''Default define directory button'''
        self.dir1 = filedialog.askdirectory(parent=self.root, initialdir="/", title='Please select a directory')
        self.svDir.set(self.dir1)
    
    def merge_options(option_a, option_b):
        "Make names from all possible matches in two lists"
        optionlist = []
        for item in option_a:
            for secondItem in option_b:
                newItem = item + secondItem
                optionlist.append(newItem)
        return optionlist


####### Run Window ###########################
root = Tk()
app = NOAA_sat_app(root)
root.mainloop()
