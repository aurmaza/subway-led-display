import json
def lambda_handler(event, context):
    print("Event received:", event)  # shows in CloudWatch logs
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from Lambda!",
            "received_event": event
        })
    }
