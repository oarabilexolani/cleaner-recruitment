from flask import Flask, render_template, request, redirect, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import smtplib

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cleaners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key")

# Initialize database
db = SQLAlchemy(app)

# Define models (Cleaner and ClientRequest)
class Cleaner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)

class ClientRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Helper function to send email
def send_email(to_email, content):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, content)
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route to index page
@app.route("/")
def index():
    return render_template("index.html")

# Route to register a cleaner via HTML form
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Extract cleaner details from form
        name = request.form["name"]
        age = request.form["age"]
        experience = request.form["experience"]
        skills = request.form["skills"]
        location = request.form["location"]
        availability = request.form["availability"]
        
        # Add cleaner to the database
        cleaner = Cleaner(
            name=name,
            age=age,
            experience=experience,
            skills=skills,
            location=location,
            availability=availability
        )
        db.session.add(cleaner)
        db.session.commit()
        
        # Send email notification to admin
        send_email("oarabilexolani2@gmail.com", f"New Cleaner Registered: {name}")
        
        flash("Cleaner registered successfully!", "success")
        return redirect("/")
    return render_template("register.html")

# Route to submit client request
@app.route("/client_request", methods=["GET", "POST"])
def client_request():
    if request.method == "POST":
        # Extract client request details from form
        experience = request.form["experience"]
        location = request.form["location"]
        requirements = request.form["requirements"]
        
        # Add client request to the database
        client_request = ClientRequest(
            location=location,
            experience=experience,
            requirements=requirements
        )
        db.session.add(client_request)
        db.session.commit()
        
        # Send email notification
        send_email("oarabilexolani2@gmail.com", f"New Client Request Submitted:\nLocation: {location}\nExperience: {experience}\nRequirements: {requirements}")
        
        flash("Client request submitted successfully!", "success")
        return redirect("/")
    return render_template("client_request.html")

# Route to admin page (after login)
@app.route("/admin")
def admin():
    if 'admin_logged_in' in session and session['admin_logged_in']:
        # Fetch all cleaners and client requests from the database
        cleaners = Cleaner.query.all()
        client_requests = ClientRequest.query.all()
        return render_template("admin.html", cleaners=cleaners, client_requests=client_requests)
    else:
        flash("You need to log in first.", "danger")
        return redirect("/admin_login")

# Admin login route
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check credentials
        if username == "oarabilexolani2@gmail.com" and password == "1234":
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect("/admin")
        else:
            flash("Invalid credentials, please try again.", "danger")

    return render_template("admin_login.html")

# Admin logout route
@app.route("/admin_logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.", "success")
    return redirect("/admin_login")

if __name__ == "__main__":
    app.run(debug=True)
