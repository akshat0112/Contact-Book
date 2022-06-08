from array import array
from operator import truediv
from re import I
from sre_constants import SUCCESS
from winreg import QueryInfoKey
from flask import Flask, render_template, redirect, url_for, request
import pymongo
import pyautogui

myclient = pymongo.MongoClient("mongodb+srv://akscontact:accesscontact@cluster0.ebe7gan.mongodb.net/test")

# create the application object
app = Flask(__name__)
@app.route('/',methods = ['GET', 'POST'])
def option():
        return render_template('options2.html')

@app.route('/osearch',methods = ['GET', 'POST'])
def search():
    if request.method== "POST":
        name=request.form['name']
        mydb = myclient["Contactbook"]
        mycol = mydb["Contact"]
        
        query = {"Name":name}
        array=list( mycol.find(query))
        listtostr = ''.join(map(str,array))
        return listtostr
    return render_template('search.html')

@app.route('/oadd',methods = ['GET', 'POST'])
def add():
    if request.method== "POST":
        name=request.form['name']
        email=request.form['email']
        number=request.form['no']

        
        mydb = myclient["Contactbook"]
        mycol = mydb["Contact"]
        data1={
                        "Name":name,
                        "Email-address":email,
                        "Contact No":number
        }
        rec_data1 = mycol.insert_one(data1)
        print("Your contact is added succesfully!! ",rec_data1)
        pyautogui.alert("You have successfully added a contact")
        return "Added Successfully"    
    return render_template('add.htmL')

@app.route('/odelete',methods = ['GET', 'POST'])
def delete():
    if  request.method== "POST":
        Name=request.form['name']
       
        mydb = myclient["Contactbook"]
        mycol = mydb["Contact"]
        query = {"Name":Name}
        array=list( mycol.find(query))
        listtostr = ''.join(map(str,array))
        mycol.delete_many(query)
        pyautogui.alert("Contacts deleted successfully")
        return ("The contact"+ listtostr + "\n\n has been deleted succesfully")

    return render_template('delete.html')

@app.route('/oreplace',methods = ['GET', 'POST'])
def replace():
    if request.method == "POST":
           name=request.form['name']
           mydb=myclient['Contactbook']
           mycol=mydb['Contact']
           number=request.form['no']
           query={"Name":name}
           numdata=mycol.find({"Contact no":number})
           
           mycol.replace_one({"Name":name}, {"Contact no":number})
           array=list(mycol.find(query))
           listtostr=''.join(map(str,array))
           return "Your updated contact is" + listtostr

    
    return render_template('modify.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)