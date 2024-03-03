from app import create_app
from app.extensions import db
from app.models import Darla, AirQuality
from app.generateID import Generate

app = create_app()

if __name__ == "__main__":
    # To remove whitespace
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=True)
