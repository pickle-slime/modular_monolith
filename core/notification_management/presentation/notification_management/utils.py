from django.conf import settings

import requests

def create_campaign(subject, from_name, reply_to, audience_id):
    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns"
    api_key = settings.MAILCHIMP_API_KEY

    data = {
        "type": "regular",
        "recipients": {
            "list_id": audience_id
        },
        "settings": {
            "subject_line": subject,
            "from_name": from_name,
            "reply_to": reply_to,
            "title": subject  # Optional: a title for your campaign
        }
    }

    headers = {
        "Authorization": f"apikey {api_key}"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.status_code, response.json()


def set_campaign_content(campaign_id, html_content):
    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/content"
    api_key = settings.MAILCHIMP_API_KEY

    data = {
        "html": html_content
    }

    headers = {
        "Authorization": f"apikey {api_key}"
    }

    response = requests.put(url, json=data, headers=headers)
    return response.status_code, response.json()


def send_campaign(campaign_id):
    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send"
    api_key = settings.MAILCHIMP_API_KEY

    headers = {
        "Authorization": f"apikey {api_key}"
    }

    response = requests.post(url, headers=headers)
    return response.status_code

def send_email_to_audience(subject, from_name, reply_to, audience_id, html_content):
    # Step 1: Create the campaign
    status_code, campaign_response = create_campaign(subject, from_name, reply_to, audience_id)
    
    if status_code == 200:
        campaign_id = campaign_response['id']

        # Step 2: Set the campaign content
        status_code, content_response = set_campaign_content(campaign_id, html_content)

        if status_code == 200:
            # Step 3: Send the campaign
            status_code = send_campaign(campaign_id)
            if status_code == 204:
                return status_code  # You can check the status here
        else:
            return content_response  # Handle content setting error
    else:
        return campaign_response  # Handle campaign creation error