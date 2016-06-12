from flask import Flask, render_template, jsonify, request
import rest_api
import register_api
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/api/<url>', methods=['GET'])
def server_api(url):
	# api/GBAbotv
	# pass
	baseurl = "http://i.imgur.com/"
	# return url
	return rest_api.call_api(baseurl + str(url) + ".jpg")

@app.route('/register/<url>')
def register(url):
	# register/GBAbotv
	# pass
	baseurl = "http://i.imgur.com/"
	return register_api.register_api(baseurl + str(url) + ".jpg")

@app.route("/apiv1/")
def apiv1():
	# apiv1/?q=http://i.imgur.com/GBAbotv.jpg
    all_args = request.args.to_dict()
    url = all_args['q']
    return rest_api.call_api(str(url))

@app.route("/registerv1/")
def registerv1():
	# registerv1/?q=http://i.imgur.com/GBAbotv.jpg
    all_args = request.args.to_dict()
    url = all_args['q']
    # return url
    return register_api.register_api(str(url))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
