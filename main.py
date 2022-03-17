#!/usr/bin/env python
# coding: utf-8

# In[28]:


import yaml
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[29]:


with open('configs.yaml', 'r', encoding='utf-8') as stream:
    try:
        configs = yaml.safe_load(stream)
    except Exception as e:
        print("Có lỗi xảy ra khi đọc file configs.yaml")
        print(str(e))


# In[30]:


configs


# In[31]:


driver = webdriver.Chrome()
driver.implicitly_wait(configs['waiting_time'])


# In[32]:


# chosen = configs['urls']['chosen']
# driver.get(configs['urls']['region'][chosen])

driver.get(configs['urls']['login_url'])
time.sleep(1)


# In[6]:


# define function
def find_element(css_selector):
    return driver.find_element(By.CSS_SELECTOR, css_selector)

def find_elements(css_selector):
    return driver.find_elements(By.CSS_SELECTOR, css_selector)

def waiting(css_selector, time=configs['waiting_time']):
    return WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )

def scroll_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# In[7]:


scroll_bottom()


# In[8]:


# button apply now
# waiting(configs['css']['apply_now_btn']).click()


# In[9]:


scroll_bottom()
# button login or create account
# find_elements(configs['css']['login_btn'])[-1].click()


# In[10]:


# switch tab
# driver.switch_to.window(driver.window_handles[-1])


# In[11]:


scroll_bottom()
# username input
waiting(configs['css']['username_txt']).send_keys(configs['authentication']['username'])
waiting(configs['css']['password_txt']).send_keys(configs['authentication']['password'])
waiting(configs['css']['submit_btn']).click() # button click submit


# # Đợi ở đây

# In[33]:


configs['submit_time']


# In[34]:


def check():
    now = datetime.now()
    return (now.hour >= configs['submit_time']['hour']) and (now.minute >= configs['submit_time']['minute'])

print("Đợi một chút")

while not check():
    time.sleep(1)
    
print("Continue")


# In[14]:


scroll_bottom()
# button submit
waiting(configs['css']['submit_process_btn']).click()


# In[16]:


waiting('input[type=checkbox]')
# list tick button
driver.execute_script("document.querySelectorAll('input[type=checkbox]').forEach((e) => e.click())")


# In[17]:


find_element('input[value=SUBMIT]').click()


# In[18]:


# pay now button
waiting('div[align=center] > table > tbody > tr > td > a').click()


# In[19]:


scroll_bottom()
# button next step
waiting(configs['css']['next_step_btn']).click()


# In[20]:


scroll_bottom()
# payer name
waiting(configs['css']['payer_name_txt']).send_keys(configs['authentication']['payer_name'])
waiting(configs['css']['ok_btn']).click() # button ok


# In[21]:


scroll_bottom()
# payment information
waiting(configs['css']['card_number_txt']).send_keys(configs['payment']['card_number'])
waiting(configs['css']['expirydate_txt']).send_keys(configs['payment']['expirydate'])
waiting(configs['css']['csc_txt']).send_keys(configs['payment']['csc'])
waiting(configs['css']['card_holder_txt']).send_keys(configs['payment']['cardholder_name'])
# button pay
waiting(configs['css']['payment_btn']).click() # button click payment

