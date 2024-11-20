import requests, datetime, csv, time, os, random, ssl

# Define constants
API_URL = 'https://www.komplett.no/api-product/SubscribeProductForm/Add'
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.komplett.no',
    'referer': 'https://www.komplett.no/product/1314319/gaming/playstation/playstation-5-pro',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
PRODUCT_ID = '1314319'

# Function to send subscription request

def random_proxy():
    try:
        pl = open("proxies.txt").readlines()
        rp = random.choice(pl).strip()
        if len(rp.split(":")) == 2:
            return {"http": f"http://{rp}", "https": f"http://{rp}"}
        elif len(rp.split(":")) == 4:
            splitted = rp.split(":")
            return {"http": "http://{0}:{1}@{2}:{3}".format(splitted[2], splitted[3], splitted[0], splitted[1]),
                    "https": "http://{0}:{1}@{2}:{3}".format(splitted[2], splitted[3], splitted[0], splitted[1]),
                    }
    except Exception as e:
        print(f'Failed to get porxie... Using local ERROR: [{e}]')
        return None


def subscribe(email):
    session = requests.session()
    get_proxy = random_proxy()
    get_ps5 = session.get("https://www.komplett.no/product/1314319/gaming/playstation/playstation-5-pro", headers=HEADERS, proxies=get_proxy)
    print(f"Get Page Status Code: {get_ps5.status_code}")
    json_data = {
        'productId': PRODUCT_ID,
        'email': email,
        'notificationType': 'PendingRelease',
    }
    print(f"Attempting subscription for: {email}")
    try:
        response = session.post(API_URL, headers=HEADERS, json=json_data, proxies=get_proxy)
        print(f"Response for {email}: {response.status_code}, {response.text}")
        if response.status_code == 200:
            return f"Success: {email}"
        else:
            return f"Failed: {email}, Status Code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error: {email}, Exception: {str(e)}"

# Main function to read emails and process requests
def main(email_file):
    print(f"Reading email file: {email_file}")
    try:
        with open(email_file, 'r') as file:
            emails = file.readlines()
        if not emails:
            print("Email file is empty. Exiting.")
            return
        results = []
        for email in emails:
            email = email.strip()  # Remove whitespace
            if email:
                result = subscribe(email)
                results.append(result)
        # Log results to a file
        with open('subscription_log.txt', 'w') as log_file:
            log_file.write('\n'.join(results))
        print("Process completed. Log saved to 'subscription_log.txt'.")
    except FileNotFoundError:
        print(f"File not found: {email_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Entry point of the script
if __name__ == '__main__':
    email_file_path = 'emails.txt'  # Replace with the path to your email file
    main(email_file_path)
