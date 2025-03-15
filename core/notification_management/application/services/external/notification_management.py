import config

import requests

class MailchipService:
    def create_campaign(self, subject, from_name, reply_to, audience_id):
        url = f"https://{config.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns"
        api_key = config.MAILCHIMP_API_KEY

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


    def set_campaign_content(self, campaign_id, html_content):
        url = f"https://{config.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/content"
        api_key = config.MAILCHIMP_API_KEY

        data = {
            "html": html_content
        }

        headers = {
            "Authorization": f"apikey {api_key}"
        }

        response = requests.put(url, json=data, headers=headers)
        return response.status_code, response.json()


    def send_campaign(self, campaign_id):
        url = f"https://{config.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send"
        api_key = config.MAILCHIMP_API_KEY

        headers = {
            "Authorization": f"apikey {api_key}"
        }

        response = requests.post(url, headers=headers)
        return response.status_code

    def send_email_to_audience(self, subject, from_name, reply_to, audience_id, html_content):
        # Step 1: Create the campaign
        status_code, campaign_response = self.create_campaign(subject, from_name, reply_to, audience_id)
        
        if status_code == 200:
            campaign_id = campaign_response['id']

            # Step 2: Set the campaign content
            status_code, content_response = self.set_campaign_content(campaign_id, html_content)

            if status_code == 200:
                # Step 3: Send the campaign
                status_code = self.send_campaign(campaign_id)
                if status_code == 204:
                    return status_code  # You can check the status here
            else:
                return content_response  # Handle content setting error
        else:
            return campaign_response  # Handle campaign creation error

    @staticmethod
    def subscribe_user_to_mailchimp(email, first_name='', last_name=''):
        api_url = f"https://{config.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{config.MAILCHIMP_AUDIENCE_ID}/members"
        api_key = config.MAILCHIMP_API_KEY

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