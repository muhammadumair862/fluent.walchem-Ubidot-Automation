#!/usr/bin/env python
# coding: utf-8

# In[12]:


from selenium import webdriver
import time
import bs4
import requests
import math
import random


# In[13]:


def txt_file():
    devices_lables=[]
    with open('devices.txt','r') as f:
        for i in f:
            devices_lables.append(i.strip())
    return devices_lables


# In[14]:


TOKEN = "ubidots Token"  # Put your TOKEN here
# DEVICE_LABEL = "ph"  # Put your device label here 
# VARIABLE_LABEL_1 = "ph"  # Put your first variable label here
# Enter username password of https://fluent.walchem.com
username="insert username"
password="insert password"
ls=[]

driver=webdriver.Chrome('chromedriver')


# In[15]:


driver.get('https://fluent.walchem.com/login.html')


# In[16]:


def credential_fun():
    time.sleep(5)
    if driver.current_url=='https://fluent.walchem.com/login.html':
        user=driver.find_element_by_id('username')
        user.send_keys(username)
        password=driver.find_element_by_id('password')
        password.send_keys(password)
        ent=driver.find_element_by_id('login_button')
        ent.click()


# In[17]:


def process_page():
    ph_list=[]
    print("process")
    if driver.current_url=='https://fluent.walchem.com/index.html':
        driver.get('https://fluent.walchem.com/index.html')
        time.sleep(5)
#         print(driver.page_source)
        page=bs4.BeautifulSoup(driver.page_source,'html')
    else:
        time.sleep(5)
        page=bs4.BeautifulSoup(driver.page_source,'html')
    ph=page.find_all('div',attrs={'class':'status'})
    
    try:
        for i in ph:
            ph_value=float(i.text)
            ph_list.append(ph_value)
    except:
        time.sleep(60)
        driver.get('https://fluent.walchem.com/index.html')
        process_page()
    print(ph_list)
    return ph_list


# In[18]:


def build_payload(value_1,device_lable):
    VARIABLE_LABEL_1=device_lable
    payload={VARIABLE_LABEL_1:value_1}
    return payload


def post_request(payload,device_lable):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, device_lable)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check             your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main(ph_value,device_lable):    # VARIABLE_LABEL_1 for variable changing
    payload = build_payload(ph_value,device_lable)

    print("[INFO] Attemping to send data")
    post_request(payload,device_lable)
    print("[INFO] finished")


# In[19]:


def get_size(l1,d1):
    size=0
    if len(l1)==len(d1):
        size=len(l1)
    else:
        size=min(len(l1),len(d1))
    return size


# In[ ]:


if __name__=='__main__':
    devices_lables=txt_file()
    while True:
        if driver.current_url=='https://fluent.walchem.com/login.html':
            credential_fun()
            ls=process_page()
            s=get_size(ls,devices_lables)
            for i in range(s):
                main(ls[i],devices_lables[i])
        elif driver.current_url=='https://fluent.walchem.com/index.html':
            l1=process_page()
            if ls!=l1:
                ls=l1.copy()
                s=get_size(ls,devices_lables)
                for i in range(s):
                    main(l1[i],devices_lables[i])
            else:
                print("Already Exist")
        time.sleep(200)




