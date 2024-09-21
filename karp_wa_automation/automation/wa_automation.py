from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import frappe
import logging
import json
import requests
import urllib.parse

erp_server_settings = frappe.get_doc('ERP Server Settings')

def send_welcome_msg():

    data = get_welcome_cust_from_server()
    print(data['message'])

    message_list = data['message']

    com_status_obj_list = []
    
    customer_data = json.loads(message_list["customer_data"])
    for customer in customer_data:
        first_name = customer.get("First Name")
        mobile_number = customer.get("Mobile Number")
        wa_template = frappe.get_doc("WA Template", {"name": "Welcome Message"})
        context = {
            "first_name": first_name
        }
        message = frappe.render_template(urllib.parse.unquote(message_list["message_template"]), context)
        result = send_automated_wa_msg(mobile_number,message)       
        if(result.get("status") == "Success"):
            com_status_obj = {
                "sales_order": customer.get("Sales Order"),
                "welcome_msg_status": "Sent"
            }
            com_status_obj_list.append(com_status_obj)
        else:
            #TODO: Implement Failure notification logic
            print("Will send Failure notification")   
    response = update_communication_status_on_server(com_status_obj_list)
    return response  
   


def get_welcome_cust_from_server():
    # You may pass headers if required
    headers = {
        "Authorization": f"token {erp_server_settings.api_key}:{erp_server_settings.api_secret}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the GET request to the API
        response = requests.get(erp_server_settings.api_url + "get_cust_for_welcome_msg", headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            # Return the parsed JSON data (you can modify this as needed)
            return data
        else:
            return {
                "status": "error",
                "message": f"Failed to fetch data from API. Status Code: {response.status_code}"
            }
    except Exception as e:
        # Log any exceptions
        frappe.log_error(message=str(e), title="API Call Failed")
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
    

#Sends WA msg using Selenium in headless mode
def send_automated_wa_msg(mobile_no, message):

    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=/Users/sushilpal/Library/Application Support/Google/Chrome/Default") 
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Path to your ChromeDriver
        chrome_driver_path = '/Users/sushilpal/Workspace/Karp/WA_Script/chromedriver' 

        # Set up ChromeDriver service
        service = Service(chrome_driver_path)

        # Create a new instance of the Chrome driver with options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        encoded_message = urllib.parse.quote(message)

        url = f"https://web.whatsapp.com/send/?phone={mobile_no}&type=phone_number&app_absent=0&text={encoded_message}"


        driver.get(url)
        wait=WebDriverWait(driver,1000)
        message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
        message_box.send_keys(Keys.ENTER)
        time.sleep(2)
        return {
            "status": "Success"
        }
    except Exception as e:
        # Log any exceptions
        frappe.log_error(message=str(e), title="Failed to send WA message for " + mobile_no)
        return {
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        }

def update_communication_status_on_server(com_status_obj_list):
    
    # You may pass headers if required
    headers = {
        "Authorization": f"token {erp_server_settings.api_key}:{erp_server_settings.api_secret}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request to the API
        response = requests.post(erp_server_settings.api_url + "update_communication_status", headers=headers, json=com_status_obj_list)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            # Return the parsed JSON data (you can modify this as needed)
            return data
        else:
            return {
                "status": "error",
                "message": f"Failed to fetch data from API. Status Code: {response.status_code}"
            }
    except Exception as e:
        # Log any exceptions
        frappe.log_error(message=str(e), title="API Call Failed")
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }

