# Module for NFC payment processing
import nfc 

def process_payment(amount):
    # Assuming the NFC device is properly set up
    clf = nfc.ContactlessFrontend('usb')
    target = clf.sense()
    if target:
        # Here you would interact with the payment service
        print(f"Processing payment of {amount} via NFC.")
        return True
    else:
        print("NFC device not detected.")
        return False
