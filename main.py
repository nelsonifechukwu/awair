from app import create_app
from app.extensions import db
from app.models import Darla, AirQuality
from app.generateID import Generate


# import ssl
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('', '')

app = create_app()
# To add a device (Test code)
# with app.app_context():
#     # db.drop_all()
#     # db.create_all()
#     device = Generate(10).id
   
#     check_device = Darla.query.filter_by(device_id = device).first()
#     while check_device is not None:
#         device = Generate(10).id
#     else:
#         print(device)
#         new = Darla(device_id = device, active=1)
#         db.session.add(new)
#         db.session.commit()

    # new = Darla(active=1)
    # db.session.add(new)
    # db.session.commit()
    # new = AirQuality(darla_id = "125749fa-fbe2-40ab-b5b1-aefd6379ab96", pmtwo=53, pmten=13, co_index=23)
    # db.session.add(new)
    # db.session.commit()
if __name__ == "__main__":
    # To remove whitespace
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    # To add functions
    
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)

# ssl_context = 'adhoc'