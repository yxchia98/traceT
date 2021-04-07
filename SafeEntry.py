from bottle import Bottle, template, request
from bottle import static_file
from datetime import datetime

app = Bottle()
locations = ['Causeway Point', 'Hillion Mall', 'Changi Jewel', 'Northpoint City', 'LotOne', 'JCube', 'WestGate',
                'VivoCity', 'CitySquare Mall', 'Bugis+', 'Bedok Mall', 'Pulau Tekong']
# Static CSS Files
@app.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

# Static JS Files
@app.route('/static/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='static/js')

@app.route('/<locationID>')
def index(locationID):
    """Home Page"""
    location = locations[int(locationID)]
    return template("enter.tpl", location=location, message="")

@app.post('/safeentry')
def checkinhandler():
    """Handle the form submission"""

    id = request.forms.get('id')
    location = request.forms.get('location')
    current = datetime.now()
    date = current.strftime('%d %B %Y')
    time = current.strftime('%I:%M %p')
    return template("safeentry.tpl", location=location, id=id, date=date, time=time, datetime=current)

@app.post('/safeout')
def checkouthandler():
    """Handle the form submission"""

    id = request.forms.get('id')
    location = request.forms.get('location')
    indatetime = request.forms.get('datetime')
    current = datetime.now()
    outdate = current.strftime('%d %B %Y')
    outtime = current.strftime('%I:%M %p')
    print(id, location, indatetime, current)
    return template("safeout.tpl", location=location, date=outdate, time=outtime)


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=8080, debug=True)
