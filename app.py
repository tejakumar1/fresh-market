from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from jinja2 import Environment, FileSystemLoader

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('main.html')


app = Flask(__name__)
# Function to send the order email
def send_order_email(customer_email, order_details):
    sender_email = os.getenv("tejakumar2121@gmail.com")
    sender_password = os.getenv("ifmwbxgycvsaqwbv")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Your Order Details"

    body = f"Thank you for your order. Here are your details:\n\n{order_details}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
    except Exception as e:
        print(f"Error: {e}")

# Route to render the HTML form
@app.route('/')
def order_form():
    return render_template('main.html')  # Make sure your HTML is saved as 'templates/index.html'

# Route to handle form submission
@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form['customer-name']
    email = request.form['customer-email']
    phone = request.form['customer-phone']
    vegetable = request.form['item-select-vegetable']
    fruit = request.form['item-select-fruit']
    meat = request.form['item-select-meat']
    quantity = request.form['quantity']

    # Format the order details for the email
    order_details = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Vegetable: {vegetable}
    Fruit: {fruit}
    Meat: {meat}
    Quantity: {quantity}
    """

    # Send the order email
    send_order_email(email, order_details)

    return redirect(url_for('order_confirmation', name=name))

# Route to display the order confirmation page
@app.route('/order-confirmation')
def order_confirmation():
    name = request.args.get('name')
    return f"<h1>Thank you, {name}! Your order has been placed successfully.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
