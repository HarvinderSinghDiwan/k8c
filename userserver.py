from flask import Flask ,request, make_response, jsonify
from flask_cors import CORS
import subprocess as sp

from time import perf_counter
app = Flask(__name__)
CORS(app)
@app.route('/userdata',methods=["POST"])
def userdata():
    fdict=request.json
    print(fdict)
    return fdict
app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc") 