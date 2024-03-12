from app import create_app
from app.extensions import db
from app.models.device import Darla 
from app.models.data import AirQuality
from app.generateID import Generate

app = create_app()

# #app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
# with app.app_context():
# #     # db.drop_all()
# #     # db.create_all()
#     device = Generate(10).id
   
#     check_device = Darla.query.filter_by(device_id = device).first()
#     while check_device is not None:
#         device = Generate(10).id
#     else:
#         print(device)
#         new = Darla(device_id = device, active=0)
#         db.session.add(new)
#         db.session.commit()

# if __name__ == "__main__":
#     # To remove whitespace
#     app.jinja_env.lstrip_blocks = True
#     app.jinja_env.trim_blocks = True
#     # To add functions
    
#     app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)