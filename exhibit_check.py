from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time 
import os, sys

def check_exhibits(driver_path, exhibit_dir, filer, pword):
    path = driver_path
    dirs = exhibit_dir
    os.chdir(dirs)
    failed = [] 
    browser=webdriver.Chrome(path)
    browser.get("https://pacer.login.uscourts.gov/csologin/login.jsf?pscCourtId=NYSDC&appurl=https://ecf.nysd.uscourts.gov/cgi-bin/showpage.pl?16")
    mouse = webdriver.ActionChains(browser) 

    browser.find_element_by_id('loginForm:loginName').send_keys(filer)
    browser.find_element_by_id('loginForm:password').send_keys(pword)
    browser.find_element_by_id('loginForm:fbtnLogin').click()
    time.sleep(2)

    browser.find_element_by_id('regmsg:chkRedact').click()
    time.sleep(1)

    browser.find_element_by_id('regmsg:bpmConfirm').click()
    time.sleep(1)

    browser.find_element_by_xpath('//*[@id="yui-gen4"]/a').click()
    browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/table/tbody/tr/td[1]/a[1]').click()

    my_dict = {"Exhibit Path": [], "Exhibit Name":[]}
    
    for f in os.listdir():
        my_dict["Exhibit Path"].append(dirs + '\\' + f)
        my_dict["Exhibit Name"].append(f)
    
    for i in range(len(my_dict["Exhibit Path"])):
        exbts_btn = browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/form/p[1]/input')
        exbts_btn.send_keys(my_dict["Exhibit Path"][i])
        browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/form/p[2]/table/tbody/tr[1]/td[1]/input').click()
        time.sleep(.5)
        
        if browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/span').text != 'The PDF document meets all CM/ECF requirements.':
            failed.append(my_dict["Exhibit Name"][i])
        
        browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/a').click()
    
    if len(failed) > 0:
        print("The following exhibits need to be fixed: ")
        for f in failed:
            print(f, '\n')
    else:
        print("All the PDFs are valid")