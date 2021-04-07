from datetime import datetime

import pymongo as pymongo
from flask import Flask, render_template, request

app = Flask(__name__)
locations = ['Causeway Point', 'Hillion Mall', 'Changi Jewel', 'Northpoint City', 'LotOne', 'JCube', 'WestGate',
             'VivoCity', 'CitySquare Mall', 'Bugis+', 'Bedok Mall', 'Pulau Tekong']


@app.route('/<int:locationID>')
def index(locationID):
    """Home Page"""
    location = locations[int(locationID)]
    return render_template("enter.html", location=location, message="")


@app.route('/safeentry', methods=['POST', 'GET'])
def checkinhandler():
    if request.method == 'POST':
        """Handle the form submission"""
        result = request.form
        current = datetime.now()
        date = current.strftime('%d %B %Y')
        time = current.strftime('%I:%M %p')
        return render_template("safeentry.html", id=result.get('id'), location=result.get('location'), date=date,
                               time=time, datetime=current)
    else:
        return render_template("safeentry.html")


@app.route('/safeout', methods=['POST', 'GET'])
def checkouthandler():
    if request.method == 'POST':
        """Handle the form submission"""
        result = request.form
        id = result.get('id')
        location = result.get('location')
        indatetime = datetime.strptime(result.get('datetime'), '%Y-%m-%d %H:%M:%S.%f')
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
        return render_template("safeout.html", location=location, date=outdate, time=outtime)
    else:
        return render_template("safeout.html")


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0') # e.g. if your machine's ipv4 is 192.168.1.15, starting url is '192.168.1.15:5000/<insert location id here>
