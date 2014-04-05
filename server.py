from flask import Flask, jsonify, request, session
import pymongo


app = Flask(__name__, static_url_path="static", static_folder="static")
app.debug = True
app.secret_key = 'WOW_SO_SECRET_ZOMG'

db = pymongo.MongoClient().user_data

@app.route('/status')
def status():
	return jsonify({'message': 'OK'})

@app.route('/add-user', methods=['POST'])
def add_user():

	# Check for correct content type
	if not request.json:
		abort(400)

	user = {'phone_number': request.json['phoneNumber'],
			'region': request.json['region']}
	db.users.insert(user)

	return jsonify({'message': 'All good!'})

if __name__ == '__main__':
	app.run() # Yeah, I know the debug server shouldn't be used in prod. This is a hackathon.
