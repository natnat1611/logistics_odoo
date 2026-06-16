from flask import Flask, render_template
from db import Session
from models import GeoZone

app = Flask(__name__)

@app.route('/zones')
def zones():
    
    try:
        zones = Session.query(GeoZone).all()
        
        return render_template('zones.html', zones=zones)
    finally:
        Session.remove()

if __name__ == '__main__':
    app.run(debug=True)