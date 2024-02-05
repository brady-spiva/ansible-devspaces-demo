# Simplified: Custom Ansible Modules
Welcome! 

This lab is designed to provide a hands-on experience with creating custom Ansible modules. These lab instructions walk you through the process of creating two custom modules to interact with MinIO: rh1.minio.**bucket** and rh1.minio.**object**. The two modules should have the following operations:

| Module |     Operations     | 
|--------|--------------------|
| Bucket | add, remove		  |
| Object | fput, fget, remove |

The main files you will need to edit include: 
<!-- add links to these files -->
- [bucket.py](plugins/modules/bucket.py)
- [object.py](plugins/modules/object.py)
- [rh1_minio_test.yml](../../../../playbooks/tasks/rh1_minio_test.yml) 

### Credentials and endpoints:
- **OpenShift Cluster URL** (will be deleted Feb. 9th): https://console-openshift-console.apps.cluster-2c6z6.2c6z6.sandbox2771.opentlc.com/
  - usernames: user{your_user_number}, e.g. user1, user2, user3, user4, user5, etc.
  - password: openshift
- **Dev Spaces URL**: https://devspaces.apps.cluster-2c6z6.2c6z6.sandbox2771.opentlc.com/
  - use your OpenShift credentials
- **MinIO Console**: https://minio-console-minio.apps.cluster-2c6z6.2c6z6.sandbox2771.opentlc.com
- **MinIO API**: minio-s3-minio.apps.cluster-2c6z6.2c6z6.sandbox2771.opentlc.com
  - **Access Key**: minioadmin
  - **Secret Key**: minioadmin
  - **Bucket Naming Convention**: ansible-test-{your_user_number} (e.g. ansible-test-1)
  - **Object Naming Convention**: test-file-object (no constraints on this)

## Getting Started 
Under the rh1.minio collection directory, go to **plugins** &rarr; **modules** &rarr; **[bucket.py](plugins/modules/bucket.py)**. The functionality to create a MinIO bucket is given to you. 
```python
def make_bucket(client, name):
# Create bucket.
	buckets = client.list_buckets()
	if name not  in buckets:
		client.make_bucket(name)
		return  "Bucket"  + name +  "was created."
	else:
		return  "Bucket"  + name +  "already exists"
```

Go to **playbooks** &rarr; **tasks** &rarr; **[rh1_minio_test.yml](../../../../playbooks/tasks/rh1_minio_test.yml).**  You should see the following play. 
```yaml
---
# code: language=ansible
- name: Testing Bucket Creation & Removal
  hosts: localhost
  vars:
    minio_url: "minio-s3-minio.apps.cluster-2c6z6.2c6z6.sandbox2771.opentlc.com"
    access_key: "minioadmin"
    secret_key: "minioadmin"
    bucket_name: "UPDATE_ME"
    object_name: "test-file-object"
  tasks:
    #### Creating a bucket
    - name: Create a bucket
      rh1.minio.bucket:
        minio_url: "{{ minio_url }}"
        access_key: "{{ access_key }}"
        secret_key: "{{ secret_key }}"
        name: "{{ bucket_name }}"
        state: present
```

Run the playbook with 
```bash
ansible-playbook rh1_minio_test.yml
```

Go to the MinIO console (play.min.io) and log in with the provided credentials. Search for your newly created bucket. 

Take a few minutes to see how the module interacts with the playbook before moving on to the next steps. 

## Extra Credit
- [ ] Add a new operation to the bucket module to list all buckets.
- [ ] Add a new operation to the bucket module to get the URL of a bucket.
- [ ] Add a new operation to the object module to list all objects in a bucket.
- [ ] Add a new operation to the object module to copy an object between buckets (or to a new bucket!).
- [ ] Add a new operation to the object module to get the URL of an object.
- [ ] Add a new operation to the object module to set the metadata of an object.
- [ ] 

## Resources
- [RH1 2024 NA Lab - Simplified: Custom Ansible Modules](https://docs.google.com/presentation/d/1sOBHXvuBTziCeVQEjvlfaGCYb1sS6xntPAlyfsDplrA/edit#slide=id.g2651b4b0f0a_0_10)
- [Ansible docs for developing custom modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
