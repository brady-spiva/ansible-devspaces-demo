#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from minio import Minio
from minio.error import S3Error
__metaclass__ = type

DOCUMENTATION = r'''
---
module: object

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule

def get_object(client, bucket, object):
    # Get object.
    try:
        response = client.get_object(bucket, object)
    # Read data from response.
    finally:
        response.close()
        response.release_conn()

def put_object(client, bucket, object, src):
    # Put object.
    # Upload unknown sized data.
    result = client.put_object(
        bucket, object, src, length=-1, part_size=10*1024*1024,
    )
    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )

def fget_object(client, bucket, object, dest):
    # Download an object file.
    client.fget_object(bucket, object, dest)

def fput_object(client, bucket, object, src):
    # Upload file 
    client.fput_object(bucket, object, src)

def remove_object(client, name):
    client.remove_object(name)

def list_object(client, bucket):
    objects = client.list_objects(bucket)
    return objects

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        bucket=dict(type='str', required=True),
        object=dict(type='str', required=True),
        src=dict(type='str', required=False), #or data
        dest=dict(type='str', required=False), 
        mode=dict(type='str', choices=['get','put', 'copy', 'list', 'remove', 'stat', 'fget', 'fput'], required=True),
    )
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    client = Minio(
        module.params['minio_url'],
        access_key=module.params['access_key'],
        secret_key=module.params['secret_key'],
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if module.params['mode'] == "get": 
        get_object(
            client=client,
            bucket=module.params['bucket'], 
            object=module.params['object']
        )
        # changed = True 
        # result['message'] = "object" + module.params['object'] + "was retrieved successfully." 
   
    elif module.params['mode'] == "put": 
        put_object(
            client=client,
            bucket=module.params['bucket'], 
            object=module.params['object'], 
            src=module.params['src']
        )

    elif module.params['mode'] == "remove": 
        remove_object(
            client=client,
            bucket=module.params['bucket'], 
            object=module.params['object']
        )

    elif module.params['mode'] == "fput": 
        fput_object(
            client=client,
            bucket=module.params['bucket'], 
            object=module.params['object'], 
            src=module.params['src']
        )
    
    elif module.params['mode'] == "fget": 
        fget_object(
            client=client,
            bucket=module.params['bucket'], 
            object=module.params['object'], 
            dest=module.params['dest']
        )

#COPY LIST STAT 

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()