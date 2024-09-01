# Module for QR code payment processing
import pyqrcode
import png
from flask import url_for

def generate_qr_code(amount):
    qr_data = f"Pay {amount}"
    qr = pyqrcode.create(qr_data)
    qr_file = f'static/qr_{amount}.png'
    qr.png(qr_file, scale=8)
    return qr_file
