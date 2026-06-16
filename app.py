from flask import Flask
from db import Session
from models import GeoZone

app = Flask(__name__)

@app.route('/zones')
def zones():
    
    try:
        zones = Session.query(GeoZone).all()
        
        return str(zones[0].zone_name)
    finally:
        Session.remove()

if __name__ == '__main__':
    app.run(debug=True)