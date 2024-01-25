# Simplified: Custom Ansible Modules
**Objective:** Create two ansible modules to interact with MinIO: bucket and object. The two modules should have the following operations:

| Module |     Operations     | 
|--------|--------------------|
| Bucket | add, remove		  |
| Object | fput, fget, remove |

The main files you will need to edit include: 
- bucket.py
- object.py 
- rh1_minio_test.yml 


## Getting Started 

Under the rh1.minio collection directory, go to **plugins** &rarr; **modules** &rarr; **bucket.py**. The functionality to create a MinIO bucket is given to you. 
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

Go to **playbooks** &rarr; **tasks** &rarr; **rh1_minio_test.yml.**  You should see the following play. 
```yaml
---
# code: language=ansible
- name: Testing Bucket Creation & Removal
  hosts: localhost
  vars:
    endpoint: "play.min.io"
    bucket_name: "ansible-test"
    object_name: "test-file-object"
    access_key: "minioadmin"
    secret_key: "minioadmin"
  tasks:
    #### Creating a bucket
    - name: Create a bucket
      rh1.minio.bucket:
        endpoint: "{{ endpoint }}"
        name: "{{ bucket_name }}"
        state: present
        access_key: "{{ access_key }}"
        secret_key: "{{ secret_key }}"
```

Run the playbook with `ansible-playbook rh1_minio_test.yml`

Go to the MinIO console (play.min.io) and log in with the provided credentials. Search for your newly created bucket. 

Take a few minutes to see how the module interacts with the playbook before moving on to the next steps. 



