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
erp_client_settings = frappe.get_doc('ERP Client Settings')

headers = {
        "Authorization": f"token {erp_server_settings.api_key}:{erp_server_settings.api_secret}",
        "Content-Type": "application/json"
    }

def init_wa():
    # Load the JSON field (assuming field name is 'key_value_data')
    store_to_profile_loc = erp_client_settings.store_to_chrome_profile_loc

    # Parse the JSON string into a Python dictionary
    store_to_profile_loc_dict = json.loads(store_to_profile_loc)
    # Iterate over key-value pairs
    for store, chorme_profile_loc in store_to_profile_loc_dict.items():
        print(f"{chorme_profile_loc}")
         # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={chorme_profile_loc}") 

        # Path to your ChromeDriver
        chrome_driver_path = erp_client_settings.chrome_driver_path

        # Set up ChromeDriver service
        service = Service(chrome_driver_path)

        # Create a new instance of the Chrome driver with options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        

        url = f"https://web.whatsapp.com/send/?type=phone_number&app_absent=0"

        driver.get(url)
        input()
        

# def send_wa_automated_msgs():
#     print("Sending WA msgs")
#     send_welcome_msg()
#     send_thankyou_msg()

def send_transactional_wa_msgs():
    print("Sending Transaction WA msgs")
    send_welcome_msg()
    send_order_ready_msg()
    send_thankyou_msg()

def send_welcome_msg():
    data = get_welcome_data_from_server()
    return process_data_and_send_msg(data, "Welcome")
    
def send_thankyou_msg():
    data = get_thankyou_data_from_server()
    return process_data_and_send_msg(data, "Thankyou")

def send_order_ready_msg():
    data = get_order_ready_data_from_server()
    return process_data_and_send_msg(data, "OrderReady")

def process_data_and_send_msg(data, message_type):

    message_list = data.get("message")

    com_status_obj_list = []
    
    customer_data = json.loads(message_list.get("customer_data"))
    
    for customer in customer_data:
        first_name = customer.get("First Name")
        mobile_number = customer.get("Mobile Number")
        loyalty_points = customer.get("Loyalty Points")
        context = {
            "first_name": first_name,
            "loyalty_points": loyalty_points
        }
        
        message = frappe.render_template(urllib.parse.unquote(message_list["message_template"]), context)

        result = send_automated_wa_msg(mobile_number,message,customer.get("Store"))   

        if(result.get("status") == "Success"):
            if(message_type == "Welcome"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "welcome_msg_status": "Sent"
                }
            elif (message_type == "Thankyou"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "thankyou_msg_status": "Sent"
                }
            elif (message_type == "OrderReady"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "order_ready_msg_status": "Sent"
                }    
            com_status_obj_list.append(com_status_obj)
        else:
            if(message_type == "Welcome"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "welcome_msg_status": "Error"
                }
            elif (message_type == "Thankyou"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "thankyou_msg_status": "Error"
                }
            elif (message_type == "OrderReady"):
                com_status_obj = {
                    "sales_order": customer.get("Sales Order"),
                    "order_ready_msg_status": "Error"
                }    
            com_status_obj_list.append(com_status_obj)      
    response = update_communication_status_on_server(com_status_obj_list)
    #Send Report
    send_automated_wa_msg("+919359234852","Automated Msg Sent","Sect 14 Gurgaon - LS") 
    return response  


def get_welcome_data_from_server(): 
    return get_data_from_server("get_data_for_welcome_msg")

def get_thankyou_data_from_server(): 
    return get_data_from_server("get_data_for_thankyou_msg")

def get_order_ready_data_from_server(): 
    return get_data_from_server("get_data_for_order_ready_msg")
    
def get_data_from_server(method):
    try:
        # Make the GET request to the API
        response = requests.get(erp_server_settings.api_url + method, headers=headers)

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
def send_automated_wa_msg(mobile_no, message,store):
    try:
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={get_chrome_profile_loc_for_store(store)}") 
        if(erp_client_settings.wa_automation_mode == "Headless"):
            chrome_options.add_argument("--headless")  # Enable headless mode
            chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
            chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Path to your ChromeDriver
        chrome_driver_path = erp_client_settings.chrome_driver_path

        # Set up ChromeDriver service
        service = Service(chrome_driver_path)

        # Create a new instance of the Chrome driver with options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        encoded_message = urllib.parse.quote(message)

        url = f"https://web.whatsapp.com/send/?phone={mobile_no}&type=phone_number&app_absent=0&text={encoded_message}"


        driver.get(url)
        wait=WebDriverWait(driver,15)
        message_box_path='//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]'
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

def get_chrome_profile_loc_for_store(store):
    
    # Load the JSON field (assuming field name is 'key_value_data')
    store_to_profile_loc = erp_client_settings.store_to_chrome_profile_loc

    # Parse the JSON string into a Python dictionary
    store_to_profile_loc_dict = json.loads(store_to_profile_loc)

    # Retrieve the value for the given key
    profile_loc = store_to_profile_loc_dict.get(store)

    return profile_loc

def update_communication_status_on_server(com_status_obj_list):
    
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



def send_marketing_msgs():

    data = get_data_from_server("get_active_wa_marketing_campaigns")

    wa_campaigns = data.get("message")

    cust_campaign_inclusion_list = []

    # Iterate over the list of campaigns and process each one
    for campaign in wa_campaigns:
        # Access fields for each campaign
        campaign_name = campaign.get('Campaign Name')  # Example: Get the 'name' field
        # campaign_status = campaign.get('status')  # Example: Get the 'status' field
        # Add more fields based on your requirements

        # Process the campaign (you can print or log information as needed)
        customers = json.loads(campaign.get('Customers'))
        
        for customer in customers:

            context = {
                "first_name": customer.get('First Name')
            }
            message = frappe.render_template(urllib.parse.unquote(campaign.get("WA Message")), context)
            # result = send_automated_wa_msg(customer.get("Mobile Number"),message,campaign.get("Store"))   
            # if(result.get("status") == "Success"):
            #     cust_campaign_inclusion = {
            #         "Campaign": campaign.get('Campaign Id'),
            #         "Customer": customer.get('Customer Name')
            #     }

            cust_campaign_inclusion = {
                "Campaign": campaign.get('Campaign Id'),
                "Customer": customer.get('Customer Name')
            }

            cust_campaign_inclusion_list.append(cust_campaign_inclusion) 

    print(cust_campaign_inclusion_list)
    update_cust_campaign_inc_on_server(cust_campaign_inclusion_list)


def update_cust_campaign_inc_on_server(cust_campaign_inclusion_list):
    
    try:
        # Make the POST request to the API
        response = requests.post(erp_server_settings.api_url + "update_cust_campaign_inc_on_server", headers=headers, json=cust_campaign_inclusion_list)

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
