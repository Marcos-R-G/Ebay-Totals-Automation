
# Ebay Payout Automation

## Description

This project was created to help a chain of retail stores seperate their sales on [Ebay](ebay.com) based on the store that put it up for sale while continuing to use the same Ebay account. The project uses [Python](python.org) and [Selenium](https://www.selenium.dev/), a browser automation tool, in conjunction with [Chrome drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) to iterate throgh every day of a given month adding up the fees and net profit or loss for each sale. 

It achieves this by checking the title for a symbol that corisponds with whatever store or individual put the item for sale. Given that symbol it will save the dollar amount it sold for, the fees for the sale, and the net profit or loss for that transaction. It will then total up the fees and net for the entire month. 

If the symbol designating the sale to an individual or store is not present it will print out that sale to the user so they can determine where the fees and net should be taken from or given to. once the total and unknown items are printed the program used [MatPlotLib](https://devdocs.io/matplotlib~3.1/) to create a pie chart displaying the percentage sales per store.

## Run Instructions

### Required External Libraries
- [Selenium](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)
- [MatPlotLib](https://matplotlib.org/stable/users/installing/index.html)

### Required Imports

``` python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import time
import sys
```

### Instructions
- Open IDE of choice
- Open EbayPayouts.py
- Run!
- On newly open chrome tab sign into eaby
- navigate to ebay payouts page
- Advanced sort and only include current month
- Click on IDE and double click enter
- Wait 3 minutes untill output.txt file and png file are saved

### Output Text File Example

<img width="955" alt="Screen Shot 2022-03-31 at 3 09 47 PM" src="https://user-images.githubusercontent.com/46509184/161152263-85217425-e1a2-4d6f-aa9d-83e9d5075b18.png">


### Output PNG File Example


<img width="640" alt="Screen Shot 2022-03-31 at 3 02 49 PM" src="https://user-images.githubusercontent.com/46509184/161149781-d04933ff-729a-44a1-8500-48481c869078.png">


> Disclamer:
> This project was super specific to this company and you would need to change symbols, XPATH, dates and many others to get running perfectly if tihs applies to you also. Thanks!

