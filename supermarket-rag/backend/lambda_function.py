import urllib.request
import json
import os

def lambda_handler(event, context):
    url = "https://xfukqtd5pc.us-east-1.awsapprunner.com/api/admin/update-catalogs"
    admin_key = os.environ.get("ADMIN_API_KEY", "5ab868c201588d172fdbe7f3e627098dc451d1cff012e03923f07f3889f03b0e")
    
    print(f"Triggering update at: {url}")
    
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", f"Bearer {admin_key}")
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"Status: {status}, Body: {body}")
            return {
                'statusCode': status,
                'body': body
            }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
