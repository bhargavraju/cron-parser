# Cron parser
Command line application that runs parsing and validation of the standard cron format with five time fields (minute, hour, day of
month, month, and day of week) plus a command

## How to run the script
1. Install the latest version of python 3, the version needs to be > 3.10
2. Verify that this version of python is installed with the command `python --version`, if the version being displayed is 2.x.x, then your system's default version in 2 so check `python3 --version` and make sure the version is above 3.10
3. Extract the zip file to a folder cron-parser
4. change directory using `cd cron-parser`
5. Use the script in the following manner `python parser.py <cron_string>` or if your system's default python version is 2, then use `python3 parser.py <cron_string>`
6. Example: `python parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"`

## Run tests
1. Execute command `pip install -r requirements.txt` to install all required packages for running tests 
2. If above step fails, manually install the minimum required libraries - pytests and ddt, with the command `pip install ddt pytest`  
3. Execute command `pytest --disable-warnings test/` to run testcases.
