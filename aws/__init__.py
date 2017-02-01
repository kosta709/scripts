import boto3, pprint, sys

C_SUCCESS = 'SUCCESS'
C_FAIL = 'FAIL'
C_TIMEOUT = 'TIMEOUT'

def log(message):
    print(message)

def add_sg(region, instance_filter, sg_ids, dryRun=False):

# ii = ec2.describe_instances(Filters=[
#         {
#             'Name': 'tag:environment',
#             'Values': [ 'aws-production']
#         },
#     ])

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


#### For Staging
'''
region = 'us-east-1'
filter = [{'Name': 'tag:environment', 'Values': [ 'aws-staging']}]
sg_ids = ['sg-d35c65aa', 'sg-ef5ed293', 'sg-95fa54e9']

import aws
aws.add_sg(region, filter, sg_ids)
'''

### Production cf-prod - us-east-1 default vpc
'''
region = 'us-east-1'
filter = [{'Name': 'tag:environment', 'Values': [ 'aws-production']}]
sg_ids = ['sg-8a26dbf0', 'sg-ef5ed293', 'sg-075bd77b']
'''