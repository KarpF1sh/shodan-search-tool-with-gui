# GUI Tool to search shodan.io
Simple python program to find things on shodan.io with a interface made with TKinter
You need, preferrably a premium Shodan.io API-key to use this. You can get one: [here](https://www.shodan.io/).  

Note: This project is quite old 

### Features
Search hosts on shodan from one or multiple pages (if you have a premium key)
Look through the data of the hosts
Export the results in to a file
Do a lookup on some specific host

### Running
On Windows open the `run.bat` file, or:  

Install the dependencies: `pip install -r requirements.txt`  
And run `python shodanv2.py` from the command line

### Building
You can also build the python application to a single executable file.
On Windows run `build.bat`    
Or run `pip install pyinstaller`  
and then `pyinstaller shodanv2.py --noconsole --onefile --icon=icon.ico`  

You can the find the file in `./dist/shodanv2.exe`  

### Issues
- Some functionality might break if using the free tier API-key
