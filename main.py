#importing python libraries that are require to build utube downloader
from pytube import YouTube 
import requests
import tkinter as tk
from tkinter.messagebox import *
from tkinter import *
from threading import *

#specifications of gui window
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 150
WINDOW_TITLE = "Youtube Video downloader"


#Accessing utube video using given api **************************************************8
#specifying body to send 
payload = { 'Gender':'All', 'MacAddress':'b8:27:eb:45:c7:21','Location':'', 'Business':'', 'Age':'' }

#sending the body using requests.post method for fetching data from API
r = requests.post("http://smartgsc.rannlabprojects.com/api/CMS/SearchAdvertisement", data = payload)

#converting fetched data to json format for easy readability
r_dict = r.json()
#specifying ID of utube video which is 12
ID = r_dict[7:9]

#specifying videourl of utube video
VideoUrl = r_dict[257:300]


class YoutubeVideosDownload:

    def __init__(self):
        #creating gui of windows application 
        self.window = tk.Tk()
        self.window.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT) )
        self.window.configure(bg="#a991c3")
        self.window.title(WINDOW_TITLE)

        #Label for video URL
        self.link_label = tk.Label(self.window, text = "Input Video URL")
        self.link_label.grid(column = 0, row = 0)
        #label for save file name as
        self.name_label = tk.Label(self.window, text = "Save File as")
        self.name_label.grid(column = 0, row = 1)
        #label for file extension
        self.ext_label = tk.Label(self.window, text = "File extension")
        self.ext_label.grid(column = 0, row = 2)

        #Inputting video URL
        self.link_entry = tk.Entry(master = self.window, width = 40)
        self.link_entry.grid(column = 1, row = 0)
        #Inputting name of file 
        self.name_entry = tk.Entry(master= self.window, width = 40)
        self.name_entry.grid(column = 1, row = 1)
        #Inputting name of extension 
        self.ext_entry = tk.Entry(master = self.window, width = 40 )
        self.ext_entry.grid(column = 1, row = 2)
        #Creating button for download videos
        self.download_button = tk.Button(self.window, text = "Download", command = self.__get_link)
        self.download_button.grid(column = 1, row = 3)
        #Creating button for AutoDownload videos
        self.autodownload_button = tk.Button(self.window, text = "AutoDownload", command = self.__autodownloader)
        self.autodownload_button.grid(column = 1, row = 4)

        return
    
    #completeDownload function to display message 'File has been downloaded' after user press Download button for downloding the video file
    def completeDownload(self,stream=None, file_path=None):
        print("download completed")
        showinfo("Message", "File has been downloaded...")
        self.link_entry.delete(0, END)
        self.name_entry.delete(0, END)

    #completeAutoDownload function to display message 'File has been downloaded' after user press AutoDownload button for downloding the video file
    def completeAutoDownload(self,stream=None, file_path=None):
        print("download completed")
        showinfo("Message", "File has been downloaded...")

    #Function __autodownloader with parameters link as VideoUrl, save_name as ID (which is 12) and default extension as mp4
    def __autodownloader(self, link=VideoUrl, save_name = ID, extension = "mp4"):
        yt = YouTube(link) 
        yt.register_on_complete_callback(self.completeAutoDownload)
        yt_stream = yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').desc().first()
        yt_stream.download(output_path = "", filename = save_name)

        return

    #Function __downloader with parameters link, save_name, and default extension as mp4
    def __downloader(self, link, save_name, extension = "mp4"):
        #if user inputs no link
        if link == '':
            self.download_button['text'] = "Input URl please..."
            return
        yt = YouTube(link)
        yt.register_on_complete_callback(self.completeDownload)
        yt_stream = yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').desc().first()
        yt_stream.download(output_path = "", filename = save_name)

        return

    #funciton __get_link that inputs link, name and ext from user
    def __get_link(self):
        link = self.link_entry.get()
        name = self.name_entry.get()
        ext = self.ext_entry.get()

        self.__downloader(link, name, ext)
        return 

    def run_app(self):
        self.window.mainloop()
        return
    

if __name__ == "__main__":
    app = YoutubeVideosDownload()
    app.run_app()