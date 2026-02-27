import boto3
import json

def check_service():
    client = boto3.client('apprunner', region_name='us-east-1')
    service_arn = 'arn:aws:apprunner:us-east-1:582604091763:service/supermarket-rag-api/bed1eb2079694639a2530c2e4e6f4624'
    
    resp = client.describe_service(ServiceArn=service_arn)
    svc = resp.get('Service', {})
    source_config = svc.get('SourceConfiguration', {})
    print(json.dumps(source_config, indent=2, default=str))

if __name__ == "__main__":
    check_service()
