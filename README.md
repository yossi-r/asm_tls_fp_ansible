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
- --TEST vulnerability – Run script (./run\_ansible.sh -q)
- --Deploy protection – Run script (./run\_ansible.sh -o)
- --TEST that the vulnerability is mitigated – Run script (./run\_ansible.sh -q)

## **Running the Demo**

### **Staging the Environment**

For F5 Engineers a UDF  **2.0**  Blueprint has been created, the main.yml, hosts, password.yml have all been configured to use UDF, you will need to modify the user\_repos.json file, as this UDF Blueprint is used for several different solutions. If you are running this demo from another environment you will need to update all these files respectively.

1. Login to UDF via Federate
2. Deploy UDF Blueprint &quot;F5 Super-NetOps &amp; Ansible MVP&quot;
3. Once deployed, make sure you start all VM&#39;s
4. Login to the Windows Host via RDP (Credentials are user/user)
5. After you are on the Windows Host open application Putty (Located on the Task Bar)
6. From the Putty window connect to the Docker Host (Credentials are ubuntu no password)



### **Using the MVP Image**

1. Launch the container with the command below from the shell window of the Docker Host
sudo docker run -p 8080:80 -p 2222:22 --rm -it -e SNOPS\_GH\_BRANCH=master f5devcentral/f5-super-netops-container:ansible

The exposed ports on the Super NetOps Container are used to interact with the solution; though the Super NetOps Container does have an exposed SSH port, we&#39;ll use the dropped into shell to run the MVP. More information on the Super NetOps Container can be found in  [F5 Programmability Lab Class 2 - Super-NetOps-Container](http://clouddocs.f5.com/training/community/programmability/html/class2/class2.html) &amp;  [F5 Docker Hub](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)


1. After the successful launch of the Super NetOps Container you should be dropped into its shell:
2. clone the repo - https://github.com/yossi-r/asm_tls_fp_ansible.git

**Updating the paramters:**
asm_tls_fp_ansible/roles/operations/defaults/main.yml
asm_tls_fp_ansible/roles/testing/defaults/main.yml
asm_tls_fp_ansible/blob/master/hosts

3. run the 
4. Return to the MVP and run the Ansible  **operations**  Playbook with Helper Script ./run\_ansible.sh -o
5. Enter the Ansible-Vault password password
6. Verify the Ansible Run success
7. Run the Ansible  **operations**  Teardown Playbook with Helper Script ./run\_ansible.sh -t
8. Enter the Ansible-Vault password password
9. Verify the Ansible Run success
10. Check BIG-IP A via the GUI for the removed objects and iApp
11. Demo complete, eat Cake.



## **Tool Kits**

### **Ansible**

F5 builds and contributes to Ansible via  [Social Coding](https://youtu.be/vTiINnsHSc4) with Github. Once a module has passed testing, it is submitted to Ansible and rolled into the next version release. F5 modules can come from software editions of Ansible (2.1,2.2,2.3 etc), or can be side-loaded by adding an Ansible library path in  [ansible.cfg](https://github.com/jmcalalang/Ansible_Meetups/blob/master/ansible.cfg). If you would like to contribute, view what&#39;s available, or acquire modules to side-load, the repository is listed below. You can also  **Watch**  this Repository for changes/fixes/additions. [F5 Network&#39;s Ansible Modules](https://github.com/F5Networks/f5-ansible/tree/devel/library)

### **F5 Super NetOps Container (Ansible Variant)**

F5 has created an MVP solution for getting up and running with Ansible and BIG-IP/iWorkflow. The MVP includes the needed dependencies such as Ansible, Python,  [f5-common-python](https://github.com/F5Networks/f5-common-python), bigsuds, etc. The MVP is delivered via code in this repository and runs within the F5 Super NetOps Container via  **Docker**. If you do not have Docker installed you can  [Install Ansible on a Mac Doc](https://github.com/jmcalalang/Ansible_Meetups/blob/master/docs/INSTALL.md) directly.

The Super NetOps Container Variant (Ansible) we will be working with can be viewed on  [Docker Hub](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)



## **Important Files within the MVP**

### **user\_repos.json File**

The user\_repos.json file is used to dynamically pull down whatever Github repository is specified in its json body. Utilizing this enables Continuously Delivery of new content every time the container is started, or the repositories are refreshed. This also allows you to specify your own downloaded/forked/cloned repository for use against your custom environment.

{

        &quot;repos&quot;: [

                {

                        &quot;name&quot;:&quot; asm\_tls\_fp\_ansible &quot;,

                        &quot;repo&quot;:&quot;https://github.com/yossi-r/asm\_tls\_fp\_ansible.git&quot;,

                        &quot;branch&quot;:&quot;master&quot;,

                        &quot;skip&quot;:false,

                        &quot;skipinstall&quot;:true

                }

        ]

}

[user\_repos.json](https://github.com/jmcalalang/Ansible_Meetups/blob/master/misc/user_repos.json)

### **Ansible Vault**

This MVP code leverages the Ansible-Vault tool, the MVP includes an encrypted password protected file  [password.yml](https://github.com/jmcalalang/Ansible_Meetups/blob/master/password.yml) for use with playbooks. The Ansible-Vault password.yml file contains the credentials of the BIG-IP we&#39;ll be working with, in our demo environment the BIG-IP credentials are &quot;admin&quot; and &quot;password&quot;, in your environment these will likely be different, change them as needed. To edit password.yml to a different username and password run the following command from the mapped repository directory in the Super NetOps Container.

ansible-vault edit password.yml

The Ansible-Vault password for the password.yml file is  **password**

### **hosts File**

The hosts file is used as a list of Ansible Inventory, in our case the MVP is configured to execute on only a single specified host, changing this file to reflect your Inventory will allow you to run this demonstration against your environment

[BIG-IPA]

10.1.1.6

[hosts](https://github.com/jmcalalang/Ansible_Meetups/blob/master/hosts)

### **main.yml File**

This file contains the variables used in the various Ansible scripts we will be executing, changing the variables in this file reflect what Ansible will deploy to a BIG-IP, for custom environments this  **will need**  to be modified. In the MVP, there are currently main.yml files for every playbook; our demo  **operations**  playbook will utilize an already configured one to create things like Nodes/Pools and Virtual Servers.

[main.yml](https://github.com/jmcalalang/Ansible_Meetups/blob/master/roles/operations/tasks/main.yml)
