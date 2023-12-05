import requests

# director
director = "Quentin Tarantino"
#topic
topic = "The Hateful Eight"



url = "https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/scriptGen"  # Replace with your API endpoint URL

# add query string parameters if needed
# convert variables to query string parameters
url += f"?director={director.replace(' ', '%20')}&topic={topic.replace(' ', '%20')}"

response = requests.get(url)

# Check the response status
if response.status_code == 200:
    print("GET request successful!")
    print("Response:", response.json())
else:
    print("GET request failed!")
    print("Status code:", response.status_code)
    print("Response:", response.text)

# get the script from the response
script = response.json()["script"] # edit the script in some way if i want
topic = topic 
directory = response.json()["folder_name"]

url = "https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/generate_video"

data = {
    "script": script,
    "topic": topic,
    "directory": directory
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.json())
else:
    print("POST request failed!")
    print("Status code:", response.status_code)
    print("Response:", response.text)
