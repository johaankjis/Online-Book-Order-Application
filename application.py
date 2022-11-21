from cs50 import sql
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

#Configuring the app
app=Flask(__name__)

#Connecting to the database
db=sql("sqlite://store.db")

#Configuring the sessions
app.config["SESSION_PERMENENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

@app.route("/")
def index():
    books=db.execute("SELECT * FROM books")
    return render_template("books.html",books=books)


@app.route("/cart",methods=["GET","POST"])
def car():
    #Checking whether the cart exist
    if "cart" not in session:
        session["cart"]=[]
    
    #POST
    if request.methods=="POST":
        id=request.form.get("id")
    if id:
        session["cart"].append(id)
        return redirect("/cart")

    #GET
    books=db.execute("SELECT * FROM books WHERE id IN(?)",session["cart"])
    return render_template("cart.html",books=books)