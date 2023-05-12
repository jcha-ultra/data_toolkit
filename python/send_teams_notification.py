import json
import requests

def send_teams_notification(fails_count, link, webhook_url):
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "title": "Test Results",
        "text": f"Number of fails: {fails_count}",
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "View Details",
                "targets": [
                    {
                        "os": "default",
                        "uri": link
                    }
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return response.status_code

WEBHOOK_URL = "your_webhook_url_here"
fails_count = 5  # Replace with the actual number of fails found in the test
link = "https://example.com/test-details"  # Replace with the actual link

status_code = send_teams_notification(fails_count, link, WEBHOOK_URL)
print(f"Notification sent with status code: {status_code}")
