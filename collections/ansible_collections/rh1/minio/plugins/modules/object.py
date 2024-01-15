#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from minio import Minio
from minio.error import S3Error
from urllib.request import urlopen
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

client = Minio("play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)

def get_object(bucket, object):
    # Get object.
    try:
        response = client.get_object(bucket, object)
    # Read data from response.
    finally:
        response.close()
        response.release_conn()

def put_object(bucket, object, src):
    # Put object.
    # Upload unknown sized data.
    src = urlopen(
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.4.81.tar.xz",
    )
    result = client.put_object(
        bucket, object, src, length=-1, part_size=10*1024*1024,
    )
    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )

def fget_object(bucket, object, dest):
    # Download data of an object.
    client.fget_object(bucket, object, dest)

def fput_object(bucket, object, src):
    result = client.fput_object(
       bucket, object, src,
    )
    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )


def remove_object(name):
    client.remove_object(name)

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

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if module.params['mode'] == "get": 
        get_object(module.params['bucket'], module.params['object'])
        # changed = True 
        # result['message'] = "object" + module.params['object'] + "was retrieved successfully." 
   
    elif module.params['mode'] == "put": 
        put_object(module.params['bucket'], module.params['object'], module.params['src'])

    elif module.params['mode'] == "remove": 
        remove_object(module.params['bucket'], module.params['object'])

    elif module.params['mode'] == "fput": 
        fput_object(module.params['bucket'], module.params['object'], module.params['src'])
    
    elif module.params['mode'] == "fget": 
        fget_object(module.params['bucket'], module.params['object'], module.params['dest'])

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