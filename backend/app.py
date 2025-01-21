# from flask import Flask, render_template, request, jsonify
# import requests

# app = Flask(__name__)

# def get_token():
#     auth_url = "https://iam.cloud.ibm.com/identity/token"
#     auth_headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     auth_data = {
#         "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
#         "apikey": "CNtTAOD3ahB5O9YzlfmXLZw2weUwHeuCuOY32uBf28g1"
#     }
    
#     response = requests.post(auth_url, headers=auth_headers, data=auth_data)
#     return response.json().get("access_token")

# def analyze_text(text):
#     token = get_token()
#     url = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/076ed571-45fc-49db-9b35-1566b67eddf2/predictions?version=2021-05-01"
    
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
    
#     input_data = {
#         "input_data": [
#             {
#                 "fields": ["sentence"],
#                 "values": [[text]]
#             }
#         ]
#     }
    
#     response = requests.post(url, headers=headers, json=input_data)
#     return response.json()

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.json
#     text = data.get('text', '')
    
#     try:
#         result = analyze_text(text)
#         prediction = result['predictions'][0]['values'][0][0]
#         probability = result['predictions'][0]['values'][0][1][0] * 100
        
#         return jsonify({
#             'success': True,
#             'prediction': prediction,
#             'probability': probability
#         })
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import requests
import datetime
import datetime


app = Flask(__name__)

# Function to get token from IBM Watson API
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
    
    if response.status_code != 200:
        print("Token retrieval failed:", response.json())
        raise Exception("Failed to retrieve access token.")
    
    return response.json().get("access_token")

# Function to analyze text using IBM Watson API
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
    
    if response.status_code != 200:
        print("API call failed:", response.json())
        raise Exception("API call failed.")
    
    return response.json()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing EULA
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        result = analyze_text(text)
        
        if 'predictions' not in result or not result['predictions']:
            raise ValueError("Unexpected response structure")
        
        prediction = result['predictions'][0]['values'][0][0]
        probability = result['predictions'][0]['values'][0][1][0] * 100
        
        analysis_data = {
            'success': True,
            'prediction': prediction,
            'probability': probability,
            'details': {
                'textLength': len(text),
                'wordCount': len(text.split()),
                'timestamp': str(datetime.datetime.now())
            }
        }
        return jsonify(analysis_data)
    
    except Exception as e:
        print(f"Error during analysis: {e}")
        return jsonify({'success': False, 'error': 'An error occurred while analyzing the EULA content. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
