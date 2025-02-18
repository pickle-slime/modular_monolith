from django.conf import settings

import requests


def subscribe_user_to_mailchimp(email, first_name='', last_name=''):
    api_url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_AUDIENCE_ID}/members"
    api_key = settings.MAILCHIMP_API_KEY

    data = {
        "email_address": email,
        "status": "subscribed", 
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name
        }
    }

    headers = {
        "Authorization": f"apikey {api_key}"
    }

    try:
        # Make the request to Mailchimp API
        response = requests.post(api_url, json=data, headers=headers, timeout=10)
        response_data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            return response.status_code, {"status": "success", "message": "You have been subscribed successfully."}
        
        # Handle potential Mailchimp API errors
        else:
            error_message = response_data.get("title")
            return response.status_code, {"status": "error", "message": error_message}

    except requests.exceptions.Timeout:
        return 504, {"status": "error", "message": "The request to Mailchimp timed out. Please try again later."}

    except requests.exceptions.RequestException as e:
        # Handle other possible request errors
        return 500, {"status": "error", "message": str(e)}