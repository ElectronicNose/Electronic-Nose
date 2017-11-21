# Electronic-Nose

This readme is created for the Electronic Nose software. The Electronic Nose software provides functionality for measuring and analyzing gas sensor data.
The application can be launched by running the file mainwindow.py in any Python IDE such as Pycharm, Spider, IDLE etc.

The following 6 python files contain the code of the project. The application has been developed using PyQt 5. 

# mainwindow_gui.py:
This file contains the code used to design the Main window. This file has been generated from the user interface file (.ui) which has been designed in Qt Designer using pyuic5 utility.

# mainwindow.py:
This file contains the code for event handling of the main window. The application can be started by running this file.

# measurement_gui.py:
This file contains the code used to design the Measurement window. This file has been generated from the user interface file (.ui) which has been designed in Qt Designer using pyuic5 utility.

# measurement.py:
This file contains code for serial communication between RPi 3 and the system microcontroller. This file also contains code for saving the measured data in a CSV file.

# analysis_gui.py:
This file contains the code to design the Analysis window. This file has been generated from the user interface file (.ui) which has been designed in Qt Designer using pyuic5 utility.

# analysis.py:
This file contains the code for back-end of the Analysis window.

PyQt 5 can be installed by entering the following command:
pip3 install pyqt5

Matplotlib can be installed by entering the following command:
python -m pip install matplotlib

numpy-1.12.0+mkl-cp36-cp36m-win32.whl (dowloaded from http://www.lfd.uci.edu/~gohlke/pythonlibs/):
pip install numpy-1.12.0+mkl-cp36-cp36m-win32.whl
	
Pyserial can be installed by entering the following command: pip install pyserial
