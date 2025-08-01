# simpleops/executor.py
from . import aws, config

current_env = "dev"

def execute(parsed_cmd, cfg):
    global current_env

    if "error" in parsed_cmd:
        return {"error": parsed_cmd["error"]}

    cmd = parsed_cmd
    if current_env not in cfg['environments']:
        return {"error": f"Environment '{current_env}' not in config"}

    env_data = cfg['environments'][current_env]

    if cmd['action'] == 'set' and cmd['target'] == 'env':
        new_env = cmd['value']
        if new_env not in cfg['environments']:
            return {"error": f"Environment {new_env} not defined"}
        if cfg['environments'][new_env].get('aws', {}).get('require_mfa'):
            mfa = input("🔐 Production env! Enter MFA token: ")
            if not mfa.isdigit() or len(mfa) != 6:
                return {"error": "Invalid MFA"}
        current_env = new_env
        return {"result": f"Environment set to {new_env}"}

    cloud_config = env_data.get(cmd['cloud'])
    if not cloud_config:
        return {"error": f"No config for cloud '{cmd['cloud']}' in env '{current_env}'"}

    region = cloud_config['region']
    profile = cloud_config.get('profile', 'default')

    if cmd['cloud'] == 'aws':
        if cmd['resource'] == 's3' and cmd['action'] == 'create':
            return aws.create_s3_buckets(cmd['bucket_name'], cmd['count'], region, profile)
        elif cmd['action'] == 'get' and cmd['resource'] == 'ec2' and cmd['field'] == 'public_ip':
            return aws.get_all_ec2_ips(region, profile)

    return {"error": f"Unsupported command: {cmd}"}
