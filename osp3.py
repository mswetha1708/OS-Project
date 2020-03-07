import tkinter 
import os     
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import threading
import time
import atexit
from tkinter import ttk
import re
flag=0
rcount=0
ind=0
threadlist=[]
lock=threading.Lock() 
class GEDIT: 
  
    __root = Tk() 
  
    # default window width and height 
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root) 
    __thisMenuBar = Menu(__root) 
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0) 
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0) 
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0) 
      
    # To add scrollbar 
    __thisScrollBar = Scrollbar(__thisTextArea)      
    __file = None
  
    def __init__(self,**kwargs): 
  
        # Set icon 
        try: 
                self.__root.wm_iconbitmap("GEDIT.ico")  
        except: 
                pass
  
        # Set window size (the default is 300x300) 
  
        try: 
            self.__thisWidth = kwargs['width'] 
        except KeyError: 
            pass
  
        try: 
            self.__thisHeight = kwargs['height'] 
        except KeyError: 
            pass
  
        # Set the window text 
        self.__root.title("Untitled - GEDIT") 
        self.__root.protocol("WM_DELETE_WINDOW", self.__quitApplication) 
        # Center the window 
        screenWidth = self.__root.winfo_screenwidth() 
        screenHeight = self.__root.winfo_screenheight() 
        flag=0
        # For left-alling 
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # For right-allign 
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # For top and bottom 
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, 
                                              self.__thisHeight, 
                                              left, top))  
  
        # To make the textarea auto resizable 
        self.__root.grid_rowconfigure(0, weight=1) 
        self.__root.grid_columnconfigure(0, weight=1) 
  
        # Add controls (widget) 
        self.__thisTextArea.grid(sticky = N + E + S + W) 
          
        # To open new file 
        self.__thisFileMenu.add_command(label="New", 
                                        command=self.__newFile)     
          
        # To open a already existing file 
        self.__thisFileMenu.add_command(label="Open", 
                                        command=self.__openFile) 
          
        # To save current file 
        self.__thisFileMenu.add_command(label="Save", 
                                        command=self.__saveFile)     
  
        # To create a line in the dialog         
        self.__thisFileMenu.add_separator()                                          
        self.__thisFileMenu.add_command(label="Exit", 
                                        command=self.__quitApplication) 
        self.__thisMenuBar.add_cascade(label="File", 
                                       menu=self.__thisFileMenu)      
          
        # To give a feature of cut  
        self.__thisEditMenu.add_command(label="Cut", 
                                        command=self.__cut)              
      
        # to give a feature of copy     
        self.__thisEditMenu.add_command(label="Copy", 
                                        command=self.__copy)          
          
        # To give a feature of paste 
        self.__thisEditMenu.add_command(label="Paste", 
                                        command=self.__paste)
        self.__thisEditMenu.add_command(label="Find", 
                                        command=self.__findbar)          
          
        # To give a feature of editing 
        self.__thisMenuBar.add_cascade(label="Edit", 
                                       menu=self.__thisEditMenu)      
          
        # To create a feature of description of the notepad 
  
        self.__root.config(menu=self.__thisMenuBar) 
  
        self.__thisScrollBar.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)      
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        t2 = threading.Thread(target=self.__multithreadautosave)
        t2.start()
        threadlist.append(t2)
        t3 = threading.Thread(target=self.__multithreadautocheck)
        t3.start()
        threadlist.append(t3)
    def __findbar(self):
    	storeobj=tkinter.Toplevel()
    	storeobj.title('Find..')
    	storeobj.transient()
    	storeobj.focus_set()
    	self.entry=tkinter.StringVar()
    	ttk.Label(storeobj, text='Find    : ').grid(row=0, column=0, padx=10, pady=10)
    	ttk.Entry(storeobj, textvariable=self.entry, width=55).grid(row=0, column=1, padx=10, pady=10)
    	ttk.Button(storeobj, text='Find',command=lambda:self.__finds(self.entry.get())).grid(column=2, row=0, padx=10, pady=10)
    	ttk.Button(storeobj, text='Close', command=lambda: storeobj.destroy()).grid(row=1, column=0, padx=10, pady=10)  	
    def __finds(self,findstr):
        print("Inside finds")
        if(len(findstr)==0):
            print("Nothing entered")
            return
        lock.acquire()
        print("Write is locked")
        file = open(self.__file,"r")
        lines=file.readlines()
        file.close()
        lock.release()
        findthreads=[]
        ###Check...................
        length=1
        for line in lines:
        	x=threading.Thread(target=self.__searchline,args=(line,findstr,length))
        	x.start()
        	length+=1
        	findthreads.append(x)
        for j in findthreads:
        	j.join(2)  
        #self.__thisTextArea.tag_add('match','1.0','1.4')
        #self.__thisTextArea.tag_config('match',foreground='red', background='yellow')     	
        #file.fseek(0,0)
        #file.write(self.__thisTextArea.get(1.0,END)) 
    def __searchline(self,line,findstr,length):
    	######NOT DONE Find findstr in line and highlight-Display position also.
    	self.__thisTextArea.tag_remove('match','1.0','end')
    	for match in re.finditer(findstr, line):
    		x=str(length)
    		x=x+'.'
    		x=x+str(match.start())
    		y=str(length)
    		y=y+'.'
    		y=y+str(match.end())
    		#indax='{}.{}'.format(x,y)
    		self.__thisTextArea.tag_add('match',x,y)
    		self.__thisTextArea.tag_config('match',foreground='red', background='yellow') 
    def __multithreadautosave(self):
    	#print("Hello")
    	global flag
    	while (flag!=1):
            time.sleep(2)
            lock.acquire()
            self.__saveFile()
            lock.release()
            #print(flag)
            time.sleep(2)
	    	#print("flag:",flag) 
    def __multithreadautocheck(self):
    	#print("Hello")
    	global flag
    	while (flag!=1):
            time.sleep(1)
            self.__misspell()
            #print(flag)
            time.sleep(2)
    def __misspell(self):
    	if(self.__file==None):
    		return
    	global ind
    	lock.acquire()
    	file2=open(self.__file,"r")
    	#print(ind)
    	file2.seek(ind,0)
    	line=file2.readline()
    	line1=line.split(" ")
    	j=len(line1)-1
    	k=line1[j]
    	line1[j]=line1[j].split("\n")
    	line1[j]=line1[j][0]
    	#print("line1[j]",line1[j])
    	ind=file2.tell()
    	if(k!=j):
    		ind=ind+1
    		#print("inside",ind)
    	#print(line1)
    	lock.release()
    	line=line.split('\n')
    	line=line[0]
    	lists=re.findall('[A-Za-z]+(?:\'[A-Za-z]+)?',str(line))
    	file=open("dictionary.txt","r")
    	lineinfile=file.readlines()
    	flagx=0
    	for item in lists:
    		item=str(item)
    		item=item.upper()
    		flagx=0
    		for linex in lineinfile:
    			linex=linex.split('\n')
    			linex=linex[0]
    			linex=str(linex)
    			if(linex==item):
    				flagx=1
    				break
    		if(flagx==0):
    			print("Misspelt",item)
    def __quitApplication(self):
    	#####Check this
    	#t2.join()
    	global flag
    	flag=1
    	print(flag)
    	threadlist[0].join(2)
    	threadlist[1].join(3)
    	print("After threads")
    	self.__root.destroy() 
   
  
    def __openFile(self): 
          
        self.__file = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
  
        if self.__file == "": 
              
            # no file to open 
            self.__file = None
        else: 
              
            # Try to open the file 
            # set the window title 
            self.__root.title(os.path.basename(self.__file) + " - GEDIT") 
            self.__thisTextArea.delete(1.0,END) 
  
            file = open(self.__file,"r") 
  
            self.__thisTextArea.insert(1.0,file.read()) 
  
            file.close() 

    def __newFile(self): 
        self.__root.title("Untitled - GEDIT") 
        self.__file = None
  
    def __saveFile(self): 
  
        if self.__file == None: 
            # Save as new file 
            self.__file = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.__file == "": 
                self.__file = None
            else: 
                  
                # Try to save the file 
                file = open(self.__file,"w") 
                file.write(self.__thisTextArea.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                self.__root.title(os.path.basename(self.__file) + " - GEDIT") 
                  
              
        else: 
            file = open(self.__file,"w") 
            file.write(self.__thisTextArea.get(1.0,END))
            file.close() 
  
    def __cut(self): 
        self.__thisTextArea.event_generate("<<Cut>>") 
  
    def __copy(self): 
        self.__thisTextArea.event_generate("<<Copy>>") 
  
    def __paste(self): 
        self.__thisTextArea.event_generate("<<Paste>>") 
  
    def run(self): 
  
        # Run main application
        self.__root.mainloop() 

        #join the threads created for autosave
    
# Run main application 
'''GEDIT = GEDIT(width=1000,height=1000) 
GEDIT.run()'''
        
if __name__ == '__main__':
   GEDIT=GEDIT(width=1000,height=1000)
   GEDIT.run()







  
    # wait until all threads finish 
    
