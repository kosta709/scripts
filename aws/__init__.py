import boto3, pprint, sys

C_SUCCESS = 'SUCCESS'
C_FAIL = 'FAIL'
C_TIMEOUT = 'TIMEOUT'

def log(message):
    print(message)


def add_sg(region, instance_filter, sg_ids, dryRun=False):

    '''
    region = 'us-east-1'
    filter = [{'Name': 'tag:environment', 'Values': [ 'aws-staging']}]
    sg_ids = ['sg-d35c65aa', 'sg-ef5ed293', 'sg-95fa54e9']

    import aws
    aws.add_sg(region, filter, sg_ids)


    ### Production cf-prod - us-east-1 default vpc
    region = 'us-east-1'
    filter = [{'Name': 'tag:environment', 'Values': [ 'aws-production']}, {'Name': 'key-name', 'Values': ['cf-prod-1']}]
    sg_ids = ['sg-8a26dbf0', 'sg-ef5ed293', 'sg-075bd77b']

    ### Production cf-prod - us-east-1  vpc-customers-01
    region = 'us-east-1'
    filter = [{'Name': 'tag:environment', 'Values': ['aws-production']}, {'Name': 'key-name', 'Values': ['cf-customers-1']}]
    sg_ids = ['sg-33d02949', 'sg-1859d564', 'sg-6450dc18']

    ### Production cf-prod - eu-central-1 default vpc
    region = 'eu-central-1'
    filter = [{'Name': 'tag:environment', 'Values': [ 'aws-production', 'aws_production']}, {'Name': 'key-name', 'Values': ['cf-prod-1']}]
    sg_ids = ['sg-8857d6e0', 'sg-9e3a22f6', 'sg-003c2468']

    ### Production cf-prod - eu-central-1 customers vpc
    region = 'eu-central-1'
    filter = [{'Name': 'tag:environment', 'Values': [ 'aws-production', 'aws_production']}, {'Name': 'key-name', 'Values': ['cf-customers-1']}]
    sg_ids = ['sg-a1a52dc9', 'sg-c33b23ab', 'sg-0731296f']
    '''

    ec2 = boto3.client("ec2", region_name=region)
    ii = ec2.describe_instances(Filters=instance_filter)
    for i in ii['Reservations']:
        instance_id = i['Instances'][0]['InstanceId']
        instance_name = [ t.get("Value") for t in i['Instances'][0]['Tags'] if t.get("Key") == "Name"]
        current_sg_ids = [sg.get('GroupId') for sg in i['Instances'][0]['SecurityGroups']]
        new_sg_ids = current_sg_ids + sg_ids

        log("updating instance {} {} - groups = {}".format(instance_id, instance_name, new_sg_ids))
        if dryRun:
            log("    skiping real update - dryRun ...\n")
            continue

        response = ec2.modify_instance_attribute(
                    DryRun=False,
                    InstanceId=instance_id,
                    Groups=new_sg_ids)


        if not response or not response.get('ResponseMetadata') or response.get('ResponseMetadata').get('HTTPStatusCode') > 299:
            raise Exception("ERROR: Invalid response from aws: {}".format(response))
            sys.exit(1)

        else:
            log("   Updated Success\n")


