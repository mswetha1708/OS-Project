# OS-Project



  TEXT EDITOR
  
  Multithreaded features Implemented:
  AutoSave- A thread will constantly save the text entered in a file until the user exits.
  AutospellCheck-The entered text is captured and misspelt word is printed in the terminal one thread per line.
  Find-One thread per line to find the character in each line.
  
  Other Non Threaded Functions:
  Open-Opens the mentioned file.
  New-Creates a new txt file in the same window.
  Cut,Copy and Paste is also done.
  
  Semaphores:
  lock() is used to lock a file as we are reading from the same file and writing into the same file while typing and checking for autospellcheck.
  
  How to Run:
  python3 osp3.py
  
  Ensure tkinter for python3 is installed.
  dictionary.txt is the text file from which misspelt words are identified(it has the words in a dictionary)
  
