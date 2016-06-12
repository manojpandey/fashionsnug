from flask import Flask, render_template
import rest_api
import register_api
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/api/<url>', methods=['GET'])
def server_api(url):
	# pass
	baseurl = "http://i.imgur.com/"
	# return url
	return rest_api.call_api(baseurl + str(url) + ".jpg")

@app.route('/test/<var>')
def test(var):
	return var

@app.route('/register/<url>')
def register(url):
	# pass
	baseurl = "http://i.imgur.com/"
	return register_api.register_api(baseurl + str(url) + ".jpg")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
