#!/bin/bash

W_USER=${W_USER:-user}
W_PASS=${W_PASS:-openshift}
GROUP_ADMINS=workshop-admins
# GROUP_USERS=workshop-users
TMP_DIR=scratch
# HTPASSWD=htpasswd-workshop-secret
WORKSHOP_USERS=50

usage(){
  echo "Workshop: Functions Loaded"
  echo ""
  echo "usage: workshop_[setup,reset,clean]"
}

doing_it_wrong(){
  echo "usage: source scripts/workshop-functions.sh"
}

is_sourced() {
  if [ -n "$ZSH_VERSION" ]; then
      case $ZSH_EVAL_CONTEXT in *:file:*) return 0;; esac
  else  # Add additional POSIX-compatible shell names here, if needed.
      case ${0##*/} in dash|-dash|bash|-bash|ksh|-ksh|sh|-sh) return 0;; esac
  fi
  return 1  # NOT sourced.
}

check_init(){
  # do you have oc
  which oc > /dev/null || exit 1

  # create generated folder
  [ ! -d ${TMP_DIR} ] && mkdir -p ${TMP_DIR}
}

workshop_create_user_htpasswd(){
  FILE=${TMP_DIR}/htpasswd
  touch ${FILE}

  which htpasswd || return

  echo "# ${W_USER}x: ${W_PASS}" > "${FILE}"

  for ((i=1;i<=WORKSHOP_USERS;i++))
  do
    htpasswd -bB "${FILE}" "${W_USER}${i}" "${W_PASS}"
  done

  echo "created: ${FILE}" 
  oc -n openshift-config create secret generic htpasswd --from-file="${FILE}"
  oc -n openshift-config set data secret/htpasswd --from-file="${FILE}"
  oc apply -f gitops/02-components/oauth.yaml

}

workshop_create_user_ns(){
  OBJ_DIR=${TMP_DIR}/users
  [ -e ${OBJ_DIR} ] && rm -rf ${OBJ_DIR}
  [ ! -d ${OBJ_DIR} ] && mkdir -p ${OBJ_DIR}

  for ((i=1;i<=WORKSHOP_USERS;i++))
  do

# create ns
cat << YAML >> "${OBJ_DIR}/${W_USER}${i}-ns.yaml"
---
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    openshift.io/display-name: Start Here - ${W_USER}${i}
  labels:
    workshop: ansible
  name: ${W_USER}${i}
---
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    openshift.io/display-name: Workspace - ${W_USER}${i}
  labels:
    workshop: ansible
  name: workspace-${W_USER}${i}
YAML

  oc apply -f "${OBJ_DIR}/${W_USER}${i}-ns.yaml"

# create rolebinding
cat << YAML >> "${OBJ_DIR}/${W_USER}${i}-admin-rb.yaml"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${W_USER}${i}-admin
  namespace: ${W_USER}${i}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: ${W_USER}${i}
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: ${GROUP_ADMINS}
YAML
  done

  # apply objects created in scratch dir
  oc apply -f "${OBJ_DIR}"

}

workshop_autoscale_test(){
  APPS_INGRESS=apps.cluster-cfzzs.sandbox1911.opentlc.com
  NOTEBOOK_IMAGE_NAME=s2i-minimal-notebook:1.2
  NOTEBOOK_SIZE="Demo / Workshop"

  for ((i=1;i<=WORKSHOP_USERS;i++))
  do

echo "---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: test
  name: ${W_USER}${i}
  namespace: sandbox
spec:
  containers:
  - name: test
    image: quay.io/devfile/universal-developer-image:ubi8-latest
    command:
      - sleep
      - infinity
    resources:
      requests:
        cpu: 500m
        memory: 8Gi
  restartPolicy: Always
" | oc apply -f -
  done
}

workshop_load_test(){

  workshop_create_user_ns

  for ((i=1;i<=WORKSHOP_USERS;i++))
  do
    oc apply -n workspace-"${W_USER}${i}" -f gitops/02-components/devspace.yaml
  done
}

workshop_load_test_clean(){
  oc delete devworkspace --all -A
  oc -n sandbox delete pod --all
}

workshop_clean_user_ns(){
  oc delete project -l workshop=ansible
  # for ((i=1;i<=WORKSHOP_USERS;i++))
  # do
  #   oc delete project "${W_USER}${i}"
  # done
}

workshop_setup(){
  check_init
  workshop_create_user_htpasswd
  workshop_create_user_ns
}

workshop_clean(){
  echo "Workshop: Clean User Namespaces"
  check_init
  workshop_clean_user_ns
}

workshop_reset(){
  echo "Workshop: Reset"
  check_init
  workshop_clean
  sleep 8
  workshop_setup
}

is_sourced && usage
is_sourced || doing_it_wrong
