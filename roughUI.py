import tkinter as tk
import scraper

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

label1 = tk.Label (root, text="API Key")
entry1 = tk.Entry (root) 
canvas1.create_window(200, 90, window=entry1)
canvas1.create_window(200, 70, window=label1)

label2 = tk.Label (root, text="Channel ID")
entry2 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry2)
canvas1.create_window(200, 120, window=label2)


def GetComments():  
    apiKey = entry1.get()
    channelId = entry2.get()
    text = tk.StringVar()
    text.set("0% Done")
    root.update()
    progress = tk.Label (root, textvariable=text)
    canvas1.create_window(200, 250, window=progress)
    scraper.getComments(apiKey,channelId, root, text)
    text.set("FINISHED")
    root.update()

    

button1 = tk.Button(text='Get All Comments', command=GetComments)
canvas1.create_window(200, 180, window=button1)


root.mainloop()






