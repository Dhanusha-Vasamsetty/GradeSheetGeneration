import qrcode


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=2,
    border=2,
)


data = "http://www.cvr.ac.in"


qr.add_data(data)
qr.make(fit=True)


img = qr.make_image()

img.save("cvr.jpg")