from datetime import datetime

import pymongo as pymongo
from bottle import Bottle, template, request
from bottle import static_file

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
    indatetime = datetime.strptime(request.forms.get('datetime'),'%Y-%m-%d %H:%M:%S.%f')
    current = datetime.now()
    outdate = current.strftime('%d %B %Y')
    outtime = current.strftime('%I:%M %p')
    client = pymongo.MongoClient(
        "mongodb+srv://Admin:UI0BvbxHM9F994HK@safetogether.wwfyn.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority")
    db = client.together
    doc = {
        'userID': int(id),
        'from': indatetime,
        'to': current,
        'location': location
    }
    db.safeEntry.insert_one(doc)

    print(id, location, indatetime, current)
    return template("safeout.tpl", location=location, date=outdate, time=outtime)


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=8080, debug=True)
