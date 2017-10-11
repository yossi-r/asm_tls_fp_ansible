## **F5 TLS fingerprint Credential stuffing mitigation - Setup and Demo**

This repository has been created to help engineers deploy and demo the F5 TLS fingerprint credential stuffing mitigation. It is not designed or tested for production use.

**Problem description:**

Automated attacks against API, specifically credentials stuffing attack against a login API.

**More details:**

Credential stuffing is one of the most popular attacks today, protecting API (not mobile API to which we have a dedicated solution) from automated attacks is challenging because it is designed for automated tools.

**The challenge:**

**App based mitigations:**

The normal way in which we stop those attacks – Using JS injections are not relevant.

Finding an HTTP object the attacker use and block it – Not effective, If you examine the HTTP portion of the request the request can look identical to a legitimate one. Attack tools have many ways to configure the HTTP request, you can manipulate headers and body and cycle through different ones.

**IP based mitigations are not effective**

It is very easy for an attacker to use a botnet with 1000&#39;s of legitimate ip endpoints sending requests (they will all have a malware installed on them)

An attacker can also use anonymous proxies to rotate ip addresses even when all requests are originating from one computer. We often see credential stuffing attacks with only several requests coming from the same ip before rotating to a new ip.

**Solution:**

In a high level, to protect from cred stuff attack we must:

1. Identify that we are under attack
  1. Identify a failed login event
  2. Either based on static threshold or a significant increase should trigger mitigations.
2. Identify an entity that&#39;s causing the attack
  1. In this case we will use SSL fingerprint
3. Block the entity
  1. Ideally do it in ASM for logs and management.

Since ip is not effective and HTTP fingerprinting isn&#39;t effective, we use SSL fingerprinting.

SSL fingerprint is a fingerprint of the &#39;client app&#39;, meaning each app has the same signature. For example chrome v47 on win10 will always have the same signature (unless someone manually changes ciphers which is very unlikely). The same way, a malware variant will always have the same fingerprint.

You can read more on ssl fingerprinting here:

[https://github.com/LeeBrotherston/tls-fingerprinting](https://github.com/LeeBrotherston/tls-fingerprinting)

[http://jis.eurasipjournals.springeropen.com/articles/10.1186/s13635-016-0030-7](http://jis.eurasipjournals.springeropen.com/articles/10.1186/s13635-016-0030-7)

The solution leverages the ssl fingerprint we extracted from the initial handshake, ASM to identify a failed login using the data guard feature. The reason we are using the dataguard feature and not the &#39;login page&#39; is that we need something that creates a violation we can track. The login page doesn&#39;t create a violation we can later use in the irule.

Step by step:

1. Identify that we are under attack
  1. Identify a failed login event

Like mentioned earlier we need to create a policy which will trigger a violation for ANY failed login. that violation will not block anything but we will use it to monitor the amount of times an identity failed to authenticate.

  - If you have session awareness enabled, make sure you disable that violation there.

We will create a data guard policy that will catch the server response of a failed login and raise a violation.
Either based on static threshold or a significant increase should trigger mitigations.

With this solution we are using static threshold that is set as a variable in the irule.

1. Identify an entity that&#39;s causing the attack
  Count the number of failed logins for each fingerprint
  Mark the entity that crossed the detection threshold

1. Block the entity
  Based on the blocked entities table in the irule we raise a custom ASM violation that will block the request.

**This Demo**

Prerequisites:

1. Bigip version 12.1+, licensed and provisioned with LTM-ASM
2. Supernetops container with ansible

We are using the bigip as the victim and the protector, the bigip token auth REST API is the victim, the solution deploys a VIP with ASM policy and an iRule to mitigate the attack.

The demo Diagram:

![image_001](/misc/images/demo_diagram.png)
### **Order of Operations**
- Deploy api_vip – Run script (./run\_ansible.sh -a)
- TEST vulnerability – Run script (./run\_ansible.sh -q)
- Deploy protection – Run script (./run\_ansible.sh -p)
- TEST that the vulnerability is mitigated – Run script (./run\_ansible.sh -q)

## **Running the Demo**

### **Staging the Environment**

1. login to the Super-NetOps-Container-ansible (More info under the tools section below)
------------------------------------------------------------------------------------------
2. clone this repo: "git clone https://github.com/yossi-r/asm_tls_fp_ansible.git"
------------------------------------------------------------------------------------------
3. go into the repo library 
------------------------------------------------------------------------------------------
4. **Update the paramters:**
  - asm_tls_fp_ansible/roles/operations/defaults/main.yml
  - asm_tls_fp_ansible/hosts
------------------------------------------------------------------------------------------
5. run the script:
- Deploy api_vip – Run script (./run\_ansible.sh -a)
- deploys the appservices template and an appservices service to expose the bigip mgmt API 
- TEST vulnerability – Run script (./run\_ansible.sh -q)
    - sends credstuff attack to the published api_vip
    - check "tailf /var/log/restjavad.0.log" on the bigip and look for the failed/success attempts
- Deploy protection – Run script (./run\_ansible.sh -p)
    - adds the fingerprint irule protection 
- TEST that the vulnerability is mitigated – Run script (./run\_ansible.sh -q)
    - sends credstuff attack to the published api_vip
    - check "tailf /var/log/restjavad.0.log" on the bigip and look for the failed/success attempts
    - check ASM event logs and look for the blocked attacks, examine the HTTP request and look for the fingerprint value in the HTTP header



## **Tool Kits**

### **Ansible**

F5 builds and contributes to Ansible via  [Social Coding](https://youtu.be/vTiINnsHSc4) with Github. Once a module has passed testing, it is submitted to Ansible and rolled into the next version release. F5 modules can come from software editions of Ansible (2.1,2.2,2.3 etc), or can be side-loaded by adding an Ansible library path in  [ansible.cfg](https://github.com/jmcalalang/Ansible_Meetups/blob/master/ansible.cfg). If you would like to contribute, view what&#39;s available, or acquire modules to side-load, the repository is listed below. You can also  **Watch**  this Repository for changes/fixes/additions. [F5 Network&#39;s Ansible Modules](https://github.com/F5Networks/f5-ansible/tree/devel/library)

### **F5 Super NetOps Container (Ansible Variant)**

F5 has created an MVP solution for getting up and running with Ansible and BIG-IP/iWorkflow. The MVP includes the needed dependencies such as Ansible, Python,  [f5-common-python](https://github.com/F5Networks/f5-common-python), bigsuds, etc. The MVP is delivered via code in this repository and runs within the F5 Super NetOps Container via  **Docker**. If you do not have Docker installed you can  [Install Ansible on a Mac Doc](https://github.com/jmcalalang/Ansible_Meetups/blob/master/docs/INSTALL.md) directly.

The Super NetOps Container Variant (Ansible) we will be working with can be viewed on  [Docker Hub](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)


### **Ansible Vault**

This MVP code leverages the Ansible-Vault tool, the MVP includes an encrypted password protected file  [password.yml](https://github.com/jmcalalang/Ansible_Meetups/blob/master/password.yml) for use with playbooks. The Ansible-Vault password.yml file contains the credentials of the BIG-IP we&#39;ll be working with, in our demo environment the BIG-IP credentials are &quot;admin&quot; and &quot;password&quot;, in your environment these will likely be different, change them as needed. To edit password.yml to a different username and password run the following command from the mapped repository directory in the Super NetOps Container.

ansible-vault edit password.yml

The Ansible-Vault password for the password.yml file is  **password**




