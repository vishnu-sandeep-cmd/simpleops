# simpleops/parser.py
import re

def parse_command(cmd: str):
    cmd = cmd.strip().lower()

    # create in aws: ec2_instance: 10
    m = re.match(r"create in (\w+): (\w+): (\d+)", cmd)
    if m:
        return {
            "action": "create",
            "cloud": m.group(1),
            "resource": m.group(2),
            "count": int(m.group(3))
        }

    # create in aws: s3: mybucket: 3
    m = re.match(r"create in (\w+): s3: ([\w\-]+): (\d+)", cmd)
    if m:
        return {
            "action": "create",
            "cloud": m.group(1),
            "resource": "s3",
            "bucket_name": m.group(2),
            "count": int(m.group(3))
        }

    # get all ec2_ip addresses
    m = re.match(r"get all ec2_ip addresses?", cmd)
    if m:
        return {
            "action": "get",
            "cloud": "aws",
            "resource": "ec2",
            "field": "public_ip"
        }

    # set env: dev
    m = re.match(r"set env: (\w+)", cmd)
    if m:
        return {
            "action": "set",
            "target": "env",
            "value": m.group(1)
        }

    return {"error": "Unrecognized command. Try: 'create in aws: ec2_instance: 1'"}
