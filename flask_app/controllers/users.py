import re
from flask_app import app
from flask import Flask, render_template, request, redirect#, session
from flask_app.models.user import User #from the models folder, we are importing our User class 

@app.route("/")
def groot():
    return redirect("/users")
#--------------------------See all users (Read)-----------------------------------
@app.route("/users")
def all_users():
    # call the query to get all the users from the get_all classmethod in the models folder 
    all_users = User.get_all()
    return render_template("index.html", all_the_users = all_users)

# ---------------------------Create new users (create)---------------------------------
@app.route("/users/new")
def new_user():
    return render_template("new_user.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "uemail" : request.form["uemail"]
    }
    # We pass the data dictionary into the save method from the User class.
    show_user = User.save(data)
    # Terminal output when creating a new user:Running Query: INSERT INTO users ( first_name , last_name , email ) VALUES ( 'NEw' , 'user' , 'user@hotmail.com' ); 11
    # The newest User's ID is being retuned in our classmethod Then we are returning the ID over to the controller. 
    # Essentially User.save(data) will become the ID returned in our classmethod, in order to use that ID we need to assign it to a variable
    # Don't forget to redirect after saving to the database. We do not render_templates on a post method
    return redirect(f"/users/{show_user}")

# --------------------------Show one users info (read one)--------------------------------------
@app.route("/users/<int:id>")
def individual(id):
    data = {
        "id": id
    }
    # call the query to get one users from the get_one classmethod in the models folder 
    one_user = User.get_one(data)
    return render_template("read_one.html", single_user = one_user)


# ---------------------------Delete users info (delete)-------------------------------------------
@app.route("/delete/<int:id>", methods = ["POST"])
def pour_a_little_out(id):
    data = {
        "id":id
    }
    User.delete(data)
    return redirect("/users")

# -----------------------------Edit Users info (Update)----------------------------------------
@app.route("/edit/<int:id>")
def edit_user(id):
    data = {
        "id": id
    }
    # We are using the same classmethod to get one user as the show one route above
    one_user = User.get_one(data)
    return render_template("edit_user.html", single_user = one_user)

@app.route("/update/<int:id>", methods = ["POST"])
def update_user(id):
    data = {
        # we need id to target a specific instance like read one and edit
        "id" : id,
        # we need to pass the request.form info over like the create route
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "uemail" : request.form["uemail"]
    }
    User.update(data)
    return redirect(f"/users/{id}")