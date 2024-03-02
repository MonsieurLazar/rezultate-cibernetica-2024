import requests
id = "9b702ddb-4432-4d7c-8602-33c757b17fe9"


url = "https://api.cyber-edu.co/v1/user/" + id

response = requests.get(url)

print(response.json()["name"])

# write it to index.html
with open("user.json", "w") as file:
    file.write(response.text)


def getName(id):
    url = "https://api.cyber-edu.co/v1/user/" + id
    response = requests.get(url)
    return response.json()["name"]
