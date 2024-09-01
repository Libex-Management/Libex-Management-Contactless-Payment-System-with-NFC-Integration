# Main Flask application
from flask import Flask, render_template, request, redirect, url_for
import nfc_payment
import qr_payment

app = Flask(__name__)

# Define a secret key for the Flask application
# This is important for security reasons when using sessions, etc.
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
def index():
    """Route for the main index page.
    This route renders the index.html template, which displays the
    options for NFC or QR code payment.
    """
    
    return render_template('index.html')

@app.route('/nfc', methods=['GET', 'POST'])
def nfc_payment_page():
    """Route for NFC payment page.
    If the request method is POST, then it checks if the 'amount' field
    is present in the form data. If it is, then it attempts to process
    the payment using nfc_payment.process_payment. If the amount is
    invalid (less than or equal to 0), or if the amount is missing, then
    it renders the NFC payment page with an appropriate error message.
    If the request method is GET, then it simply renders the NFC payment
    page.
    """
    if request.method == 'POST':
        # Check if the 'amount' field is present in the form data
        if 'amount' in request.form:
            try:
                amount = float(request.form['amount'])
                if amount <= 0:
                    # Handle invalid amount
                    return render_template('nfc_payment.html', error='Invalid amount')
                success = nfc_payment.process_payment(amount)
                if success:
                    return redirect(url_for('success'))
                else:
                    return redirect(url_for('failure'))
            except ValueError:
                # Handle invalid amount format
                return render_template('nfc_payment.html', error='Invalid amount format')
        else:
            # Handle missing 'amount' field
            return render_template('nfc_payment.html', error='Missing amount')
    return render_template('nfc_payment.html')

@app.route('/qr', methods=['GET', 'POST'])
def qr_payment_page():
    """Route for QR code payment page.

    If the request method is POST, then it checks if the 'amount' field
    is present in the form data. If it is, then it attempts to generate
    a QR code for the given amount using qr_payment.generate_qr_code.

    :param amount: The amount of the payment to be made
    :type amount: float
    If the amount is invalid (less than or equal to 0), or if the amount
    is missing, then it renders the QR payment page with an appropriate
    error message. If the request method is GET, then it simply renders
    the QR payment page.

    """
    if request.method == 'POST':
        # Check if the 'amount' field is present in the form data
        if 'amount' in request.form:
            try:
                amount = float(request.form['amount'])
                if amount <= 0:
                    # Handle invalid amount
                    return render_template('qr_payment.html', error='Invalid amount')
                qr_code = qr_payment.generate_qr_code(amount)
                return render_template('qr_payment.html', qr_code=qr_code)
            except ValueError:
                # Handle invalid amount format
                return render_template('qr_payment.html', error='Invalid amount format')
        else:
            # Handle missing 'amount' field
            return render_template('qr_payment.html', error='Missing amount')
    return render_template('qr_payment.html')

@app.route('/success')
def success():
    """Route to return if payment succeeds."""
    return "Payment Successful!"

@app.route('/failure')
def failure():
    """Route to return if payment fails."""
    return "Payment Failed!"

if __name__ == '__main__':
    app.run(debug=True)