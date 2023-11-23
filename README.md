# COMP0066_Humanitarian_Management_System

This application is created by Group 11.

%description% blablabla

The core features of this application can be run without installation. 
***However, without installation, external library will not be installed automatically, 
and the data visualisation feature will not work and could lead to unexpected error.***
Although you can install those third-parties libraries manually, 
it is recommended to install our application through pip install, and run our app through the command shown below.

After installation, the application can be accessed in any directory at anytime with the command:
```shell
hmsGroup11
```

## Installation Guide

### Double-click Installation
- Windows

Windows users can install the application via double-click on ```Installation_Win.bat```.

- Mac

Mac users can install the application via double-click on ```Installation_Mac.applescript```,
and then press the button ```▶ (Run the Script)```.

If the installation could not work properly, you can install it manually through Terminal/CMD/PowerShell.
See next section.

### Manual Installation

Before manual installation, user has to copy the absolute path to the project directory 
***Humanitarian_Management_System***:

- On windows:
Open File Explorer and navigate to the directory contains the application package, 
right-click on the package and select ```copy as path```

- On Mac:
Open Finder and navigate to the directory contains the application package, 
while holding ```option```, right-click on the package and select ```Copy "pkg" as Pathname```

After copying the absolute path,
open ```Terminal``` on Mac, or ```PowerShell```/```Command Prompt``` on Windows, then run the following pip command:
(```{local/path/to/package}``` is the path you copied in the previous step)
```shell
pip install {local/path/to/package}
```

### To launch the application

Once the application is installed, the application can be run at anytime by 
executing the following command on Terminal or Command Prompt:
```shell
hmsGroup11
```

### To launch the application without pip installation

If the installation is somehow failed, the application can still be run by the following steps:
1. Open Terminal/CMD/PowerShell.
2. Enter to the project directory using ```cd```.
3. Enter ```pip install -r requirements.txt```
4. Enter ```python -m humanitarian_management_system.main.py``` on Windows 
or ```python3 -m humanitarian_management_system.main.py``` on Mac.

Note that once you run the application thought command ```hmsGroup11```, you should not run the application again by
```python -m humanitarian_management_system.main.py``` and vice-versa. 
(The command ```hmsGroup11``` will use the data stored in python site-package as data source while 
the command ```python -m humanitarian_management_system.main.py``` will use the data stored in the local package).

### Common Issues
If ```pip: command not found``` error occurs, most of the time it is because of the missing environment variables. 
i.e. python and pip are not in ```PATH```. This can be solved by either reinstall Python and tick the option 
```Add Python to PATH```, or manually add Python and pip to ```PATH```.


## Notes for Developers

Before configuration, it is recommended to create a ***virtual environment*** and 
install dependencies only in the virtual environment.

To install dependencies, run the command below in terminal with activated venv:
```shell
pip install -r requirements.txt
```
Developers can also pip-install the package into their virtual environment by:
```shell
pip install -e.
```
