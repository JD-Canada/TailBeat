Steps to get TailBeat.py up and running on a fresh Anaconda install:

1. Go to www.continuum.io/downloads, and choose Python 2.7 64-bit installer. Install by following unscreen instructions. If asked, allow Anaconda to be default python editor/interpreter.

2. Go to opencv.org/downloads.html, and choose version 2.4.12 for Windows

3. Click on opencv-2.4.12.exe and extract to C: directory

4. Copy cv2.pyd located in C:\opencv\build\python\2.7\x64\ to C:\Users\Jason\Anaconda2\Lib\site-packages, replace "Jason" with your user name.
   Anaconda2 might be named something different(like Anaconda), but \Lib\site-packages should be the same.

5. Test cv2 install by opening Spyder (start menu, and find the program Spyder under Anaconda) and typing "import cv2" at top of blank file and run the file (green play button)
   If it installed correctly, then you will not see any errors in the console (buttom right window by default).

6. In "System properties", click on Environment variables to edit them. Create a new variable with variable name "OPENCV_DIR", without the qoutes and variable value "C:\opencv\build\x64\vc12"

7. Click to edit PATH variable and add %OPENCV_DIR%\bin at the end of the line, use ";" to seperate %OPENCV_DIR%\bin from last entry, e.g. %somethingelse%;%OPENCV_DIR%\bin, click ok

8. Find a good example tailbeat video (only one fish, nice tailbeat and no glare to begin with) and place it in your TailBeat directory. Change file name on line 5 of TailBeat.py.

9. Run TailBeat.py, hopefully everything works. If not, let me know and I will have a look.

10. If everything works, feel the circle radius "r" located on line 26, this makes the encompassing circle larger or smaller

11. Play around in fft.py to try and get out a meaningful psd and evaluate the tailbeat signal in the graphs