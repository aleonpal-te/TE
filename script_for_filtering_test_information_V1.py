import requests
import json
import base64
import csv
import os

""" Looking at the documentation for this API it seems the only responses are in JSON format, so receiving HTML is strange.
To increase the likelihood of receiving a JSON response, you can set the 'Accept' header to 'application/json'.
"""

# Get tests ID:


def get_tests_info(user, token):

    url = "https://api.thousandeyes.com/v6/tests"
    payload = {}

    credentials = user + ":" + token
    credentials_encoded = base64.b64encode(
        credentials.encode()
    ).decode()  # the authentication header must be on base64 to be able to send it
    headers = {
        "Accept": "application/json"
    }  # Forcing the accept to the API to send it in json format.
    headers["Authorization"] = "Basic " + str(credentials_encoded)

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    testid = []

    for i in response.values():

        for i2 in i:

            testid.append(i2.get("testId"))

    return testid


def get_test_name(user, token, testid):

    url = "https://api.thousandeyes.com/v6/tests/%s.json" % testid

    payload = {}

    credentials = user + ":" + token

    credentials_encoded = base64.b64encode(
        credentials.encode()
    ).decode()  # the authentication header must be on base64 to be able to send it

    headers = {
        "Accept": "application/json"
    }  # Forcing the accept to the API to send it in json format.

    headers["Authorization"] = "Basic " + str(credentials_encoded)

    response = requests.request("GET", url, headers=headers, data=payload)

    response = response.json()

    values_to_csv = []

    for i in response.values():

        for i2 in i:

            values_to_csv.append(i2.get("testName"))
            values_to_csv.append(i2.get("testId"))
            values_to_csv.append(i2.get("createdDate"))
            values_to_csv.append(i2.get("createdBy"))
            values_to_csv.append(i2.get("modifiedDate"))
            values_to_csv.append(i2.get("modifiedBy"))
            values_to_csv.append(i2.get("type"))
            values_to_csv.append(i2.get("protocol"))
            values_to_csv.append(i2.get("url"))
            values_to_csv.append(i2.get("enabled"))
            values_to_csv.append(i2.get("alertsEnabled"))

    return values_to_csv


if __name__ == "__main__":

    user_api = input("Please enter the username:")

    token_api = input("Please enter the API token of the authentication account:")

    get_tests_id = get_tests_info(user_api, token_api)

    with open("csv_file_tests_general_info.csv", "w", newline="") as csv_file:

        writer = csv.writer(csv_file)

        header = [
            "Test name",
            "Test ID",
            "Created Date",
            "Created By",
            "Modified Date",
            "Modified By",
            "Type of Test",
            "Protocol used in the Test",
            "URL",
            "Enabled",
            "Alerts in Test",
        ]

        writer.writerow(header)

        writer.writerow("")

        for test in get_tests_id:

            csv_file_data_general_info = get_test_name(user_api, token_api, test)
            
            writer.writerow(csv_file_data_general_info)

        csv_file.close()
