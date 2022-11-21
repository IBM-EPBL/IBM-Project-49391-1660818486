from flask import Flask, render_template, request
import requests


API_KEY = "eJtq0iryC5KHdxl8bvueo_ggjM6gOQGlFGqwVAfWvJ5q"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
@app.route('/')
@app.route('/checkEligibility')
def checkEligibility():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    greScore = int(request.form['gre'])
    toeflScore = int(request.form['ielts'])
    univRank = int(request.form['university rank'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = int(request.form['research paper'])
    array_of_input_fields = ['greScore', 'toeflScore', 'univRank', 'sop', 'lor', 'cgpa', 'research']
    array_of_values_to_be_scored = [greScore, toeflScore, univRank, sop, lor, cgpa, research]
    payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f4104242-d8ce-4409-86ee-94ceb3f85d0e/predictions?version=2022-11-21', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0]
    
    if prediction:
        return render_template('chance.html')
    else:
        return render_template('noChance.html')


if __name__ == "__main__":
    app.run()