## IC 1 ##
## Part 1
# What's the issue with the code below?
#   The data is not getting passed in as json put as form data 

import requests

payload = {"username": "admin", "password": "letmein"}

response1 = requests.post(
    "https://httpbin.org/post",
    data=payload,
    headers={"Content-Type": "application/json"},
)

print(response1.json())

## Part 2
# Fix the request so it sends actual JSON.

payload = {"username": "admin", "password": "letmein"}

response2 = requests.post(
    "https://httpbin.org/post",
    json=payload,
    headers={"Content-Type": "application/json"},
)
print(response2.json())

## Part 3
# Create a custom header.
payload = {"username": "admin", "password": "letmein"}
headers = {
    "Content-Type": "application/json"
}

response3 = requests.post(
    "https://httpbin.org/post",
    json=payload,
    headers=headers,
)
print(response3.json())

# Add this to your headers:
# "X-Course": "COS 542"

payload = {"username": "admin", "password": "letmein"}
headers = {
    "X-Course": "COS 542"
}

response = requests.post(
    "https://httpbin.org/post",
    json=payload,
    headers=headers,
)
print(response.text)

# Use .text or .json() to print the full response
# and confirm your data and custom header were received.