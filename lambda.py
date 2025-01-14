import boto3
import botocore
import json

APPLICABLE_RESOURCES = ["AWS::EC2::SecurityGroup"]

REQUIRED_PERMISSIONS = [
{
    "IpProtocol" : "tcp",
    "FromPort" : 22,
    "ToPort" : 22,
    "UserIdGroupPairs" : [],
    "IpRanges" : [{"CidrIp" : "0.0.0.0/0"}],
    "PrefixListIds" : [],
    "Ipv6Ranges" : []
}]

def normalize_parameters(rule_parameters):
    for key, value in rule_parameters.items():
        normalized_key=key.lower()
        normalized_value=value.lower()

        if normalized_value == "true":
            rule_parameters[normalized_key] = True
        elif normalized_value == "false":
            rule_parameters[normalized_key] = False
        elif normalized_value.isdigit():
            rule_parameters[normalized_key] = int(normalized_value)
        else:
            rule_parameters[normalized_key] = True
    return rule_parameters

def evaluate_compliance(configuration_item, debug_enabled):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return {
            "compliance_type" : "NOT_APPLICABLE",
            "annotation" : "The rule doesn't apply to resources of type " +
            configuration_item["resourceType"] + "."
        }

    if configuration_item["configurationItemStatus"] == "ResourceDeleted":
        return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": "The configurationItem was deleted and therefore cannot be validated."
        }

    group_id = configuration_item["configuration"]["groupId"]
    client = boto3.client("ec2");

    try:
        response = client.describe_security_groups(GroupIds=[group_id])
    except botocore.exceptions.ClientError as e:
        return {
            "compliance_type" : "NON_COMPLIANT",
            "annotation" : "describe_security_groups failure on group " + group_id
        }
        
    if debug_enabled:
        print("security group definition: ", json.dumps(response, indent=2))

    ip_permissions = response["SecurityGroups"][0]["IpPermissions"]
    authorize_permissions = [item for item in REQUIRED_PERMISSIONS if item not in ip_permissions]
    revoke_permissions = [item for item in ip_permissions if item not in REQUIRED_PERMISSIONS]

    if authorize_permissions or revoke_permissions:
        annotation_message = "Permissions were modified."
    else:
        annotation_message = "Permissions are correct."

    if authorize_permissions:
        if debug_enabled:
            print("authorizing for ", group_id, ", ip_permissions ", json.dumps(authorize_permissions, indent=2))

        try:
            client.authorize_security_group_ingress(GroupId=group_id, IpPermissions=authorize_permissions)
            annotation_message += " " + str(len(authorize_permissions)) +" new authorization(s)."
        except botocore.exceptions.ClientError as e:
            return {
                "compliance_type" : "NON_COMPLIANT",
                "annotation" : "authorize_security_group_ingress failure on group " + group_id
            }

    if revoke_permissions:
        if debug_enabled:
            print("revoking for ", group_id, ", ip_permissions ", json.dumps(revoke_permissions, indent=2))

        try:
            client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=revoke_permissions)
            annotation_message += " " + str(len(revoke_permissions)) +" new revocation(s)."
        except botocore.exceptions.ClientError as e:
            return {
                "compliance_type" : "NON_COMPLIANT",
                "annotation" : "revoke_security_group_ingress failure on group " + group_id
            }

    return {
        "compliance_type": "COMPLIANT",
        "annotation": annotation_message
    }

def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    configuration_item = invoking_event["configurationItem"]
    rule_parameters = normalize_parameters(json.loads(event["ruleParameters"]))

    debug_enabled = False

    if "debug" in rule_parameters:
        debug_enabled = rule_parameters["debug"] 

    if debug_enabled:
        print("Received event: " + json.dumps(event, indent=2))

    evaluation = evaluate_compliance(configuration_item, debug_enabled)

    config = boto3.client('config')

    response = config.put_evaluations(
       Evaluations=[
           {
               'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
               'ComplianceResourceId': invoking_event['configurationItem']['resourceId'],
               'ComplianceType': evaluation["compliance_type"],
               "Annotation": evaluation["annotation"],
               'OrderingTimestamp': invoking_event['configurationItem']['configurationItemCaptureTime']
           },
       ],
       ResultToken=event['resultToken'])