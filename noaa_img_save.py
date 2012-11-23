from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import os
import time
import re

#### Test Data
# testhtml = '<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_ABQ_vis.jpg">20121115_1500_ABQ_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">103K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_ABQ_wv.jpg">20121115_1500_ABQ_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">107K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_AK_ir.jpg">20121115_1500_AK_ir.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right">158K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_AK_irbw.jpg">20121115_1500_AK_irbw.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right">116K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_AK_vis.jpg">20121115_1500_AK_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">120K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_AK_wv.jpg">20121115_1500_AK_wv.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right">147K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_COD_ir.jpg">20121115_1500_COD_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">101K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_COD_irbw.jpg">20121115_1500_COD_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 74K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_COD_vis.jpg">20121115_1500_COD_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">101K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_COD_wv.jpg">20121115_1500_COD_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 73K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_DEN_ir.jpg">20121115_1500_DEN_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">113K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_DEN_irbw.jpg">20121115_1500_DEN_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 76K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_DEN_vis.jpg">20121115_1500_DEN_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">103K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_DEN_wv.jpg">20121115_1500_DEN_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 92K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_HI_ir.jpg">20121115_1500_HI_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">158K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_HI_irbw.jpg">20121115_1500_HI_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">101K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_HI_vis.jpg">20121115_1500_HI_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 98K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_HI_wv.jpg">20121115_1500_HI_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">138K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LAS_ir.jpg">20121115_1500_LAS_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">150K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LAS_irbw.jpg">20121115_1500_LAS_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">101K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LAS_vis.jpg">20121115_1500_LAS_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">105K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LAS_wv.jpg">20121115_1500_LAS_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">125K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LWS_ir.jpg">20121115_1500_LWS_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">116K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LWS_irbw.jpg">20121115_1500_LWS_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 85K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LWS_vis.jpg">20121115_1500_LWS_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">104K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_LWS_wv.jpg">20121115_1500_LWS_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 92K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_PIR_ir.jpg">20121115_1500_PIR_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 96K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_PIR_irbw.jpg">20121115_1500_PIR_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 68K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_PIR_vis.jpg">20121115_1500_PIR_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 95K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_PIR_wv.jpg">20121115_1500_PIR_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 82K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_US_ir.jpg">20121115_1500_US_ir.jpg</a></td><td align="right">15-Nov-2012 15:28  </td><td align="right">426K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_US_irbw.jpg">20121115_1500_US_irbw.jpg</a></td><td align="right">15-Nov-2012 15:28  </td><td align="right">304K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_US_vis.jpg">20121115_1500_US_vis.jpg</a></td><td align="right">15-Nov-2012 15:28  </td><td align="right">337K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_US_wv.jpg">20121115_1500_US_wv.jpg</a></td><td align="right">15-Nov-2012 15:27  </td><td align="right">421K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_WMC_ir.jpg">20121115_1500_WMC_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">123K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_WMC_irbw.jpg">20121115_1500_WMC_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 87K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_WMC_vis.jpg">20121115_1500_WMC_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 99K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_WMC_wv.jpg">20121115_1500_WMC_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 93K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_ABQ_ir.jpg">20121115_1500_sm_ABQ_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 88K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_ABQ_irbw.jpg">20121115_1500_sm_ABQ_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 59K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_ABQ_vis.jpg">20121115_1500_sm_ABQ_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 68K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_ABQ_wv.jpg">20121115_1500_sm_ABQ_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 74K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_AK_ir.jpg">20121115_1500_sm_AK_ir.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right">102K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_AK_irbw.jpg">20121115_1500_sm_AK_irbw.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right"> 75K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_AK_vis.jpg">20121115_1500_sm_AK_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 75K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_AK_wv.jpg">20121115_1500_sm_AK_wv.jpg</a></td><td align="right">15-Nov-2012 15:29  </td><td align="right"> 98K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_COD_ir.jpg">20121115_1500_sm_COD_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 66K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_COD_irbw.jpg">20121115_1500_sm_COD_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 51K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_COD_vis.jpg">20121115_1500_sm_COD_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 67K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_COD_wv.jpg">20121115_1500_sm_COD_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 51K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_DEN_ir.jpg">20121115_1500_sm_DEN_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 74K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_DEN_irbw.jpg">20121115_1500_sm_DEN_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 51K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_DEN_vis.jpg">20121115_1500_sm_DEN_vis.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 67K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_DEN_wv.jpg">20121115_1500_sm_DEN_wv.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 64K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_HI_ir.jpg">20121115_1500_sm_HI_ir.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right">103K</td></tr><tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="20121115_1500_sm_HI_irbw.jpg">20121115_1500_sm_HI_irbw.jpg</a></td><td align="right">15-Nov-2012 15:13  </td><td align="right"> 66K</td></tr>'
# soup = BeautifulSoup(testhtml) # test soup

#### Live Data
url = 'http://www.aviationweather.gov/adds/data/satellite/'
# url = 'http://www.aviationweather.gov/data/obs/sat/intl/'

get_thumbnails = False # get small or large images
timedelay = 60 * 60 # how long until getting next images
run_how_many_times = 8

area = ['COD', 'DEN', 'ABQ']
imgtype = ['_ir.jpg', '_irbw.jpg', '_vis.jpg', '_wv.jpg']


def filewriter(myfilename):
    '''Writes file to disk'''
    my_path = 'img/' + myfilename
    d = os.path.dirname(my_path)
    if not os.path.exists(d):
        os.makedirs(d)
    f = open(my_path,'wb')   # create new file locally
    f.write(urlopen(url + myfilename).read()) # Open remote file, write to newly created file
    f.close() # close file from memory

def find_and_write(area, imgtype):
    '''Find my images on a page'''
    noaa_sat = urlopen(url) # retrieve page
    html = noaa_sat.read() # make page readable
    page = html.decode("utf8") # not sure if this is really needed, but decode to utf8
    soup_var = BeautifulSoup(page) # create soup list
    # Define Search Patterns
    if get_thumbnails: # get small images
        pattern = re.compile(r'' + area + imgtype)
    else: # get large images
        pattern = re.compile(r'(?<!sm_)' + area + imgtype)
    
    anchor_tags = soup_var.findAll('a', text=pattern) # find all relevant <a> tags
    existing_files = os.listdir('img/') # check existing files
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
        filewriter(img) # run filewriter function
        print(img) # tell me what the shitshow is going on in console.
        print(str(count) + " images left") # console counter

def run_satellite_function(area_index=0, imgtype_index=0):
    '''Run the the entire scrape and print results'''
    mycount = run_how_many_times
    for gather_imgs in range(run_how_many_times):
        mycount -= 1
        print("Running")
        find_and_write(area[area_index], imgtype[imgtype_index]) # run function with specific type
        # Finished with current time, log and wait
        timestamp = time.localtime()
        print("\n\n-------------------------------")
        print("---Images Downloaded ----------\n-------------------------------")
        if run_how_many_times > 1: # check if run more than once
            print("This will run %s more times\n-------------------------------" % str(mycount))
            print("Next Download at %s:%s" % (str(timestamp[3]+1), str(timestamp[4])))
            time.sleep(timedelay) # Sleep for time interval

######### RUN THOU FUNCTION #############
run_satellite_function(2, 2) 