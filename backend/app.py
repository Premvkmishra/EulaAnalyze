from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_token():
    auth_url = "https://iam.cloud.ibm.com/identity/token"
    auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": "CNtTAOD3ahB5O9YzlfmXLZw2weUwHeuCuOY32uBf28g1"
    }
    
    response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    return response.json().get("access_token")

def analyze_text(text):
    token = get_token()
    url = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/076ed571-45fc-49db-9b35-1566b67eddf2/predictions?version=2021-05-01"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    input_data = {
        "input_data": [
            {
                "fields": ["sentence"],
                "values": [[text]]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=input_data)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    try:
        result = analyze_text(text)
        prediction = result['predictions'][0]['values'][0][0]
        probability = result['predictions'][0]['values'][0][1][0] * 100
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'probability': probability
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)