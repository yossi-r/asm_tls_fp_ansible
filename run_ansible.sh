#!/bin/bash

while test $# -gt 0; do
        case "$1" in
                -h|--help)
                        echo " "
                        echo "options:"
                        echo "-h, --help                show brief help"
                        echo "-q,                       run the credential stuffing attack"
                        echo "-a,                       create api_vip with asm policy"
                        echo "-p,                       add the protection configuration"
                        echo "-t,                       run the teardown playbook"
                        exit 0
                        ;;
                -a)
                        shift
                        ansible-playbook playbooks/operations.yml --tags api_vip_protect --ask-vault-pass -e @password.yml -e state="present" -vvv
                        shift
                        ;;
                -p)
                        ansible-playbook playbooks/operations.yml --tags protection --ask-vault-pass -e @password.yml -e state="present" -vvv
                        shift
                        ;;
                -q)
                        ansible-playbook playbooks/operations.yml --tags integration_test --ask-vault-pass -e @password.yml -e state="present" -vvv
                        shift
                        ;;
                -t)
                        ansible-playbook playbooks/operations.yml --ask-vault-pass -e @password.yml -e state="absent" -vvv
                        shift
                        ;;
                *)
                        break
                        ;;
        esac
done
