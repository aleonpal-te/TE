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


# Get additional specific tests information like agents name and shared accounts on the test.


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


def get_agents_names(user, token, testid):

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

    agent_name_list = []
    agent_type = []

    for i in response.values():

        for i2 in i:

            for i3 in i2.get(
                "agents"
            ):  # We enter the agent section of the tests details.

                agent_name_list.append(i3.get("agentName"))

                agent_type.append(i3.get("agentType"))

    return (agent_name_list, agent_type)


def get_shared_account_groups(user, token, testid):

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

    shared_accounts = []

    for i in response.values():

        for i2 in i:

            for i4 in i2.get(
                "sharedWithAccounts"
            ):  # We enter the shared account section of the tests details.

                if i4.get("name") != None:

                    shared_accounts.append(i4.get("name"))

    return shared_accounts


if __name__ == "__main__":

    user_api = input("Please enter the email of your username:")
    token_api = input("Please enter the API token of the authentication account:")

    get_tests_id = get_tests_info(user_api, token_api)

    with open("csv_file.csv", "w", newline="") as csv_file:

        fieldnames = [
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
            "Agent Name",
            "Agent Type",
            "Shared with Account",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for test in get_tests_id:  # This FOR is to fill the data per TestID.

            csv_file_data_general_info = get_test_name(user_api, token_api, test)

            csv_file_get_agents_names, csv_files_get_agents_types = get_agents_names(
                user_api, token_api, test
            )
            length_agents = len(csv_file_get_agents_names)

            csv_file_get_shared_accounts = get_shared_account_groups(
                user_api, token_api, test
            )
            length_shared_accounts = len(csv_file_get_shared_accounts)

            writer.writerow(
                {
                    "Test name": csv_file_data_general_info[0],
                    "Test ID": csv_file_data_general_info[1],
                    "Created Date": csv_file_data_general_info[2],
                    "Created By": csv_file_data_general_info[3],
                    "Modified Date": csv_file_data_general_info[4],
                    "Modified By": csv_file_data_general_info[5],
                    "Type of Test": csv_file_data_general_info[6],
                    "Protocol used in the Test": csv_file_data_general_info[7],
                    "URL": csv_file_data_general_info[8],
                    "Enabled": csv_file_data_general_info[9],
                    "Alerts in Test": csv_file_data_general_info[10],
                }
            )

            if length_agents > length_shared_accounts:

                for na in range(length_agents):

                    if csv_file_get_shared_accounts == ValueError or IndexError:

                        csv_file_get_shared_accounts.append("")

                    writer.writerow(
                        {
                            "Agent Name": csv_file_get_agents_names[na],
                            "Agent Type": csv_files_get_agents_types[na],
                            "Shared with Account": csv_file_get_shared_accounts[na],
                        }
                    )

            else:

                for na in range(length_shared_accounts):

                    if csv_file_get_agents_names == ValueError or IndexError:

                        csv_file_get_agents_names.append("")
                        csv_files_get_agents_types.append("")

                    writer.writerow(
                        {
                            "Agent Name": csv_file_get_agents_names[na],
                            "Agent Type": csv_files_get_agents_types[na],
                            "Shared with Account": csv_file_get_shared_accounts[na],
                        }
                    )

            

    csv_file.close()
    print("The file will be saved in the working directory:" + str(os.getcwdb()))
