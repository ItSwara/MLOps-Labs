import requests
import json

url = 'http://127.0.0.1:8080/predict'

payload = {
    'bill_length_mm':    39.1,
    'bill_depth_mm':     18.7,
    'flipper_length_mm': 181.0,
    'body_mass_g':       3750,
    'island':            'Torgersen',
    'sex':               'Male'
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print("Status:", response.status_code)
print("Body:",   response.text)

if response.status_code == 200:
    try:
        result     = response.json()
        prediction = result['prediction']
        confidence = result['confidence']
        print(f"Predicted species : {prediction}")
        print(f"Confidence        : {confidence}%")
    except Exception as e:
        print("Could not parse JSON:", e)
else:
    print('Error:', response.status_code)