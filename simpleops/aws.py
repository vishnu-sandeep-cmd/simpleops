# simpleops/aws.py
import boto3
import random

def get_client(service, region=None, profile=None):
    session = boto3.Session(profile_name=profile)
    return session.client(service, region_name=region)

def create_s3_buckets(base_name, count, region="us-east-1", profile="default"):
    s3 = get_client('s3', region, profile)
    created = []
    for i in range(count):
        suffix = random.randint(1000, 9999)
        bucket_name = f"{base_name}-{suffix}" if count > 1 else base_name
        try:
            if region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            created.append(bucket_name)
        except Exception as e:
            return {"error": str(e)}
    return created

def get_all_ec2_ips(region="us-east-1", profile="default"):
    ec2 = get_client('ec2', region, profile)
    resp = ec2.describe_instances()
    ips = []
    for reservation in resp['Reservations']:
        for inst in reservation['Instances']:
            if inst.get('PublicIpAddress'):
                ips.append(inst['PublicIpAddress'])
    return ips
