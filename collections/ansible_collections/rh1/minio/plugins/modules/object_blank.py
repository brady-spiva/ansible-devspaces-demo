#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from ansible.module_utils.basic import AnsibleModule
from minio import Minio
from minio.commonconfig import CopySource
from minio.error import (InvalidResponseError, S3Error)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: object

short_description: A module for creating and removing bucket_names in Minio

version_added: "1.0.0"

description: Ansible custom module for interacting with MinIO to put, get, remove, list, and copy objects.

options:
    endpoint: 
        description: The MinIO server endpoint.
        required: true
        type: str
    
    access_key: 
        description: The access key for authentication.
        required: true
        type: str 
    
    secret_key: 
        description: The secret key for authentication.
        required: true
        type: str 
    
    mode:
        description: The desired state of the MinIO object (put, get, remove, list, copy).
        required: true
        type: str 

    bucket_name: 
        description: The MinIO bucket name
        required: true
        type: str 

    object: 
        description: The MinIO object name
        required: true
        type: str 

    src: 
        description: The content to be uploaded (for put operation).
        required: false
        type: str 

    src_bucket_name: 
        description: The source bucket for copy operation.
        required: false
        type: str 

    src_object: description: The source object for copy operation.
        required: false
        type: str 
    

author:
    - Karenna Rodriguez (@ykarennarod)
'''

EXAMPLES = r'''
# Upload an object to a bucket
- name: Upload an object
  rh1.minio.object:
    endpoint: {{ endpoint }}
    access_key: {{ access_key }}
    secret_ket: {{ secret_key }}
    bucket_name: rh1_bucket
    object: rh1_object
    mode: fput

# TODO: Provide an example of how to fget an obect

# TODO: Provide an example of how to remove a bucket

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
msg:
    description: The output msg that the module generates.
    type: str
    returned: always
    sample: "MinIO object {object} uploaded to {bucket_name} successfully."
'''

def fput_object(module, client, bucket_name, object, src):
    """
    Put MinIO object of unknown size in specified bucket.

    Args:
      - module: Ansible module instance.
      - client: MinIO client instance.
      - bucket_name: Name of the MinIO bucket.
      - objec: Name of the MinIO object.
      - src: Content to be uploaded. 

    Returns:
      - Tuple: (success: bool, msg: str)
    """
    try:
        client.fput_object(bucket_name, object, src)
        return True, f'MinIO object {object} uploaded to {bucket_name} successfully.'
    except InvalidResponseError as e: 
        return False, str(e)

def fget_object(client, bucket_name, object, dest):
    # TODO: Implement the fget functionality. The required paramaters are given to you 

def remove_object(client, bucket_name, object):


# EXTRA
def list_object(module, client, bucket_name):
    # TODO

def copy_object(module, client, bucket_name, object, src_bucket_name, src_object):
    # TODO 

def run_module():
    
    # TODO_1: Define all of the parameters needed to run the object module, bucket_name is provided for you. 
    
    module_args = dict(
        bucket_name=dict(type='str', required=True),
        # object=dict(type='str', required=False),
        # src=dict(type='str', required=False), 
        # mode=dict(type='str', choices=['copy', 'list', 'remove', 'fget', 'fput'], required=True),
        # access_key=dict(type='str', required=True),
        # secret_key=dict(type='str', required=True),
        # endpoint=dict(type='str', required=True),
        # dest=dict(type='str', required=False), 
    )

    result = dict(
        changed=False,
        msg=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    
    client = Minio(
        module.params['endpoint'],
        access_key=module.params['access_key'],
        secret_key=module.params['secret_key'],
    )

    if module.check_mode:
        result['changed'] = True
        module.exit_json(**result)

    if module.params['mode'] == "remove": 
        success, msg = remove_object(
            module=module,
            client=client,
            bucket_name=module.params['bucket_name'], 
            object=module.params['object']
        )
        result['msg'] = msg

    elif module.params['mode'] == "fput": 
        success, msg = fput_object(
            module=module,
            client=client,
            bucket_name=module.params['bucket_name'], 
            object=module.params['object'], 
            src=module.params['src']
        )
        result['msg'] = msg
    
    elif module.params['mode'] == "fget": 
        success, msg = fget_object(
            module=module,
            client=client,
            bucket_name=module.params['bucket_name'], 
            object=module.params['object'], 
            dest=module.params['dest']
        )
        result['msg'] = msg

    elif module.params['mode'] == "list": 
        success, msg = list_object(
            module=module,
            client=client,
            bucket_name=module.params['bucket_name'], 
        )
        result['msg'] = msg
    
    elif module.params['mode'] == "copy": 
        success, msg = copy_object(
            module=module,
            client=client,
            bucket_name=module.params['bucket_name'], 
            object=module.params['object'], 
            src_bucket_name=module.params['src_bucket_name'], 
            src_object=module.params['src_object'], 
        )
        result['msg'] = msg

    # Register success or failure 
    if success:
        result['changed'] = True
    else:
        result['msg'] = f"Failed to perform MinIO operation: {msg}"
        module.fail_json(**result)
        
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()