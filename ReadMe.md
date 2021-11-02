# Web Coding Challenge - Python
Challenge reference is https://github.com/dusts66/coding_challenge

## Contents in the Submission
main.py is the main code
templates/index.html is a simple webform to upload a file (.tsv)
static/files/ is the location where the uploaded file is placed
requirements.txt is the pip related installables


## Pre-requisites to execute code (Windows)
1. Install Python 3.x and make sure pip works in the command line (Power shell recommended with virtual environment for Python)
1. Open Power shell as Administrator and ```pip install virtualenv ``` and set the Security policy as RemoteSigned
    ```
    PS C:\code> Get-ExecutionPolicy
    Restricted
	
	PS C:\code> Set-ExecutionPolicy RemoteSigned

	Execution Policy Change
	The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose you to the security risks described in the about_Execution_Policies help topic at
	https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
	[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): y
	
	PS C:\code> Get-ExecutionPolicy
	RemoteSigned
	
    ```
1. Create and activate Virtual environment venv3
```python venv venv3
   PS C:\code> .\venv3\Scripts\activate``` 

1. Install the required libraries
   ```pip install -r requirements.txt```

1. Download mysql 8.0.* from mysql downloads (.msi preferably) and install mysql developer option with root password as 'mysql'
   After install, launch Mysql workbench and Create a Database and create a table
   ```
   create database tsvdata;

   create table details(
   item_id INT NOT NULL AUTO_INCREMENT,
   item_name VARCHAR(100) NOT NULL,
   item_description VARCHAR(500) NOT NULL,
   item_price VARCHAR(40),
   item_count VARCHAR(40),
   vendor VARCHAR(100),
   vendor_address VARCHAR(500),
   PRIMARY KEY ( item_id )
	);

	\* This is needed to make sure mysql native authentication  by password works *\
	ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mysql';
   ``` 


## Understanding the Code layout
When we execute main.py Flask server runs on port 5000.
And the URL is accessible thru http://127.0.0.1:5000
Code sections are uploadFile method to handle file upload, parseTSV does the bulk of operation
  parseTSV method parses the data from given input file, inserts to details table in the database
  and reads overall data and makes the computation. And displays generated file of data.html in a new web browser. 


## Execution
```
   autopep8 -i main.py   # to auto python lint of code changes and make sure inconsistent tabs and spaces are auto fixed

   python main,py        # actual execution
```

data.html is created displayed in new web browser