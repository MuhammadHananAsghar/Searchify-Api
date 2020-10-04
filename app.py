from flask import Flask,render_template,jsonify,request
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/")
def route():
	return render_template("index.html")

@app.route("/api",methods=['GET','POST'])
@cross_origin()
def SearchQuery():
	query = request.args.get('query')
	headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"}
	if " " in query:
		query = query.split(" ")
		query = [i.capitalize() for i in query]
		query = "_".join(query)
	else:
		query = query
	url = f"https://en.wikipedia.org/wiki/{query}"
	soup = BeautifulSoup(requests.get(url,headers=headers).content,"lxml")
	all_text = []
	for i in soup.find_all("p"):
		all_text.append(i.text.strip())
	string = "".join(all_text)
	if len(string) > 100:
		string_data = {
		"Query": query,
		"Description": string,
		"status":200
		}
	else:
		string_data = {
		"Query": query,
		"Description": "Nothing Found",
	}

	return jsonify(string_data)


if __name__ == "__main__":
	app.run(debug=True)
