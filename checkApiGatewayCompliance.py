import json
import boto3
waf_client = boto3.client('wafv2')

def lambda_handler(event, context):
    
    web_acl_to_attach_by_default = "web_acl_arn"
    messageTye = event['detail']['messageTye']

    resourceType = event['detail']['configurationItem']['resourceType']
    if "AWS:ApiGateway" in resourceType :
        resource_arn = event['detail']['configurationItem']['ARN']
        response = waf_client.get_web_acl_for_resource(
            ResourceArn = resource_arn
        )
        
        if "WebACL" not in response :
            try :
                attachResponse = waf_client.associate_web_acl(
                    WebACLArn = web_acl_to_attach_by_default,
                    ResourceArn = resource_arn
                )
                print("Successfully attached WebACL ["+web_acl_to_attach_by_default+"] to Resource ["+resource_arn+"]")
                return True
            except Exception as e:
                print("Unable to attach Resource ["+resource_arn+"]" to WebACL ["+web_acl_to_attach_by_default+"]")
                return False
