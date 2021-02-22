import pandas as pd
import joblib
from flask import Flask, request
from flask_cors import CORS

class modelfull(object):
    def __init__(self):
            print("Initializing")
            # Variables needed for metric collection
            self.V3=0
            self.V4=0
            self.V10=0
            self.V11=0
            self.V12=0
            self.V14=0
            self.V17=0
            self.Amount=0
            self.proba_1 = 0
            #///////// Loading mode from filesystem
            self.clf = joblib.load('modelfull.pkl')
            print("Model uploaded to class")
    
    #def predict(self,x):
    def predict(self,x):
        print(x)
        print(type(x))
        result = "PASS"
        featurearray=[float(i) for i in x.split(',')]
        print(featurearray)
        # grabbing features for metric to be scraped by prometheus
        self.V3 = featurearray[0]
        self.V4 = featurearray[1]
        self.V10 = featurearray[2]
        self.V11 = featurearray[3]
        self.V12 = featurearray[4]
        self.V14 = featurearray[5]
        self.V17 = featurearray[6]
        self.Amount = featurearray[7]
        
        rowdf = pd.DataFrame([featurearray], columns = ['V3','V4','V10','V11','V12','V14','V17','Amount'])
        print(rowdf)
        self.proba_1 = self.clf.predict_proba(rowdf)[:,1]
        predictions = self.clf.predict(rowdf)
        # initialize list of lists
        result = "Proba=" + str(self.proba_1)
        return result


########
# Code #
########
# Main Flask app
app = Flask(__name__)
CORS(app)

model = modelfull()

@app.route("/", methods=["POST"])
def home():
    input_data = request.json
    prediction = model.predict(input_data['strData'])

    return prediction

# Launch Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080')
