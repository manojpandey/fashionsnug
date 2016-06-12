from flask import Flask, render_template
import rest_api

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/api/<url>', methods=['GET'])
def server_api(url):
	# pass
	# url = "https://avatars0.githubusercontent.com/u/4750240?v=3&s=460"
	baseurl = "http://i.imgur.com/"
	# return url
	return rest_api.call_api(baseurl + str(url) + ".jpg")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
