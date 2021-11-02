from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

import pandas as pd
import mysql.connector
import webbrowser

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="tsvdata",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
    print(x)


# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
       # set the file path
        uploaded_file.save(file_path)
        parseTSV(file_path)
       # save the file
    return redirect(url_for('index'))

"""
  This method parses the data from given input file, inserts to details table in the database
  and reads overall data and makes the computation. And displays generated file of data.html in a new web browser    
"""
def parseTSV(filePath):
    # TSV Column Names
    # Item  Item_description  Item_price  Item_count  Vendor  Vendor_address
    col_names = ['item', 'desc', 'price', 'count', 'vendor', 'vendor_address']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, sep="\t", names=col_names, header=None)
    # Loop through the Rows
    result = []
    for i, row in csvData.iterrows():
        # ignore 1st line since header
        if i == 0:
            continue
        sql = "INSERT INTO details (item_name, item_description, item_price, item_count, vendor, vendor_address) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (row['item'], row['desc'], str(row['price']),
                 str(row['count']), row['vendor'], row['vendor_address'])
        mycursor.execute(sql, value)
        # check for cursor execution failure
        data = "error"  # initially just assign the value
        for j in mycursor:
            data = j  # if cursor has no data then loop will not run and value of data will be 'error'
        if data == "error":
            print(
                "Item details insertion created a problem and will not be inserted; ", row)
        mydb.commit()
        print(i, row['item'], row['desc'], row['price'],
              row['count'], row['vendor'], row['vendor_address'],)
    # now read complete from DB to compute total
    query = """select * from details; """
    mycursor.execute(query)
    rows = mycursor.fetchall()
    cumulative = 0
    p = []
    tbl = "ItemItem_descriptionItem_priceItem_countVendorVendor_address"
    p.append(tbl)

    for row in rows:
        # item price * item count
        cumulative = cumulative + float(row[2]) * float(row[3])

        # add all rows to result
        a = "%s"%row[0]
        p.append(a)
        b = "%s"%row[1]
        p.append(b)
        c = "%s"%row[2]
        p.append(c)
        d = "%s"%row[3]
        p.append(d)
        e = "%s"%row[4]
        p.append(e)
        f = "%s"%row[5]
        p.append(f)

    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                  <html>
                  <head>
                  <meta content="text/html; charset=ISO-8859-1"
                  http-equiv="content-type">
                  <title>Python Webbrowser</title>
                  </head>
                  <body>
                  <table>
                  %s
                  </table>
                  <div>
                  Total of Cumulative Item Price and Count is %s 
                  </div>
                  </body>
                  </html>
                  '''%(p, cumulative)

    filename = "data.html"
    output = open(filename,"w")
    output.write(contents)
    output.close()
    # display the generated file in a new web browser
    webbrowser.open(filename)  
    
if (__name__ == "__main__"):
    app.run(port=5000)
