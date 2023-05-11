from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import time
import sys

opts = Options()
opts.add_experimental_option('debuggerAddress', '127.0.0.1:9250')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']


def clean_text(string):  # Removes unwanted chars from string
    remove = ['$', ',']
    if string == "" or string == '–':
        return float("0")
    for value in remove:
        string = string.replace(value, '')
    return float(string)


def adjust_zoom():  # Changes the zoom on the chrome settings to desired percentage
    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(.5);')


def payout_table():  # Puts the payout date, id, and amount into an iterable dict
    empty_list = []
    list_of_dicts = []
    rows = driver.find_elements(By.XPATH, '//*[@id="grid-table-root"]')
    for row in rows:
        t = row.find_elements(By.CSS_SELECTOR, "td")  # Grabs each row from the table
        for i in range(len(t)):  # Creates a list of all the rows in the table
            empty_list.append(t[i].text)
        i = 0
        while i < (len(empty_list) - 5):  # Creates a dictionary from each item list of row based on title
            copy_empty_dict = {
                "payout_date": empty_list[i],
                "payout_id": empty_list[i + 1],
                "amount": clean_text(empty_list[i + 5])
            }
            list_of_dicts.append(copy_empty_dict)
            i = i + 6

    return list_of_dicts


def clean_description(description):  # Accounts for different errors that may occur in getting the titles
    description_list = list(map(str.strip, description.split('\n')))
    # print(description_list)
    if str(description_list[0]).startswith('Order '):
        if str(description_list[2]).endswith('-') or str(description_list[2]).endswith('~') or str(description_list[2]).endswith('-') or str(description_list[2]).endswith('^') or str(description_list[2]).endswith('*'):
            return str(description_list[2])
        else:
            pass

    if str(description_list[0]).startswith('Shipping label for order'):
        usps_label = list(map(str.strip, str(description_list[0]).split(' ')))[-1]
        url = 'https://www.ebay.com/sh/ord/details?orderid=' + usps_label
        driver.get(url)
        time.sleep(.025)
        # table = driver.find_element(By.XPATH, '//*[@id="s0"]/div[1]/div[1]/div[2]/table')
        # table_row = table.find_elements(By.CSS_SELECTOR, "tr") #tbody
        # # print(len(table_row))
        # if len(table_row) >= 6:
        #     return str(description_list[len(description_list) - 2])
        title = driver.find_element(By.CSS_SELECTOR, '#itemInfo')
        title_text = title.find_element(By.CSS_SELECTOR, '#itemInfo > div > div > div > div.lineItemCardInfo__summary > div.lineItemCardInfo__text > a')
        return title_text.text
    if str(description_list[0]).startswith('Hold'):
        return str(description_list[0])

    if str(description_list[2]).endswith('item)') or str(description_list[2]).endswith('items)'):
        return "Multiple items"
    if str(description_list[0]).endswith('Box'):
        label = list(map(str.strip, str(description_list[0]).split(' ')))[-1]
        url = 'https://www.ebay.com/sh/ord/details?orderid=' + label
        driver.get(url)
        title = driver.find_element(By.CSS_SELECTOR, '#s0')
        title_text = title.find_element(By.XPATH, '//*[@id="s0-1-4-16-74-9[0]"]/td[2]/div/p[1]/span[2]')
        url = 'https://www.ebay.com/itm/' + str(title_text.text).replace("(", "").replace(")", "")
        driver.get(url)
        title = driver.find_element(By.CSS_SELECTOR, '#LeftSummaryPanel > div.vi-swc-lsp > div:nth-child(1)')
        title_text = title.find_element(By.CSS_SELECTOR, "h1")
        return title_text.text

    if str(description_list[0]).startswith('Transfer'):
        return "Transfer"


    if str(description_list[0]).startswith('Refund'):
        return "REFUND"
    if str(description_list[0]).startswith('Shipping label for item') or str(description_list[0]).startswith('USPS Short Paid Fee') or str(description_list[0]).startswith('Insertion Fee for item number') :
        fedex_label = list(map(str.strip, str(description_list[0]).split(' ')))[-1]
        url = 'https://www.ebay.com/itm/' + fedex_label
        driver.get(url)
        time.sleep(.025)
        title = driver.find_element(By.CSS_SELECTOR, '#LeftSummaryPanel > div.vi-swc-lsp > div:nth-child(1)')
        title_text = title.find_element(By.CSS_SELECTOR, "h1")
        return title_text.text
    if str(description_list[0]).startswith('Shipping label (voided)'):
        label = list(map(str.strip, str(description_list[0]).split(' ')))[-1]
        url = 'https://www.ebay.com/sh/ord/details?orderid=' + label
        driver.get(url)
        time.sleep(.025)
        title = driver.find_element(By.CSS_SELECTOR, '#itemInfo > div > div > div > div.lineItemCardInfo__summary > div.lineItemCardInfo__text')
        title_text = title.find_element(By.CSS_SELECTOR,
                                        "#itemInfo > div > div > div > div.lineItemCardInfo__summary > div.lineItemCardInfo__text > a")
        return title_text.text

    elif str(description_list[len(description_list) - 2]) == 'opens in a new window or tab':
        id = list(map(str.strip, str(description_list[0]).split(' ')))[-1]
        url = 'https://www.ebay.com/sh/ord/details?orderid=' + id
        driver.get(url)
        time.sleep(.025)
        title = driver.find_element(By.CSS_SELECTOR, '#itemInfo')
        title_text = title.find_element(By.CSS_SELECTOR,
                                        '#itemInfo > div > div > div > div.lineItemCardInfo__summary > div.lineItemCardInfo__text > a')
        return title_text.text
    return str(description_list[len(description_list) - 2])


def fees_net():  # itterates through dictionary and goes into each link to see what the title is and adds up total

    fees_per_store = {"hurricane": 0, "700": 0, "sunset": 0, "washington": 0}
    net_per_store = {"hurricane": 0, "700": 0, "sunset": 0, "washington": 0}

    empty_list = []
    list_of_dicts = []
    rows = driver.find_elements(By.XPATH, '//*[@id="grid-table-root"]')
    for row in rows:
        t = row.find_elements(By.CSS_SELECTOR, "td")  # Grabs each row from the table
        for i in range(len(t)):  # Creates a list of all the rows in the table
            empty_list.append(t[i].text)
        i = 0
        while i < (len(empty_list) - 6):  # Creates a dictionary from each item list of row based on title
            month = empty_list[0][0:3]
            prev_month = ""
            for z in range(len(months)-1):
                if months[z] == month:
                    prev_month = months[z-1]

            while empty_list[i][0:3] != month and empty_list[i][0:3] != prev_month:
                i += 1
            copy_empty_dict = {
                "date": empty_list[i],
                "description": clean_description(empty_list[i + 2]),
                "amount": clean_text(empty_list[i + 3]),
                "fees": clean_text(empty_list[i + 4]),
                "net": clean_text(empty_list[i + 5])

            }
            list_of_dicts.append(copy_empty_dict)
            i = i + 5
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]["description"][-1] == "*":  # for hurricane
            fees_per_store["hurricane"] += list_of_dicts[i]["fees"]
            net_per_store["hurricane"] += list_of_dicts[i]["net"]

        elif list_of_dicts[i]["description"][-1] == "~":  # for 700
            fees_per_store["700"] += list_of_dicts[i]["fees"]
            net_per_store["700"] += list_of_dicts[i]["net"]

        elif list_of_dicts[i]["description"][-1] == "-":  # for sunset
            fees_per_store["sunset"] += list_of_dicts[i]["fees"]
            net_per_store["sunset"] += list_of_dicts[i]["net"]

        elif list_of_dicts[i]["description"][-1] == "^":  # for washington
            fees_per_store["washington"] += list_of_dicts[i]["fees"]
            net_per_store["washington"] += list_of_dicts[i]["net"]

        else:
            print(list_of_dicts[i]["date"],
                  list_of_dicts[i]["description"],
                  list_of_dicts[i]["amount"],
                  list_of_dicts[i]["fees"],
                  list_of_dicts[i]["net"])

    return fees_per_store, net_per_store


def pie_chart(var1, var2, var3):
    labels = 'Hurricane', 'Sunset', 'Wash/700'
    sizes = [int(var1), int(var2), int(var3)]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig("ebay_payouts_piechart_.png")


def net_fees_total(list_of_dicts):  # list is list of dicts [ {key: value}, {key: value} ]
    fees_total = {"hurricane": 0, "700": 0, "sunset": 0, "washington": 0}
    net_total = {"hurricane": 0, "700": 0, "sunset": 0, "washington": 0}
    for i in range(len(list_of_dicts)):  # Checks and grabs each dict from list {key: value}
        for key in list_of_dicts[i]:  # Goes through each key inside of the dict
            if key == "payout_id":  # Checks to see if the key you are looking at is the payoutid
                payouturl = 'https://www.ebay.com/sh/fin/payout?transactionType=PAYOUT&payoutId=' + list_of_dicts[i][
                    "payout_id"] + '&uuId=' + list_of_dicts[i][
                                "payout_id"] + '&from=PAYOUTS&history=true&fromQueryString=%3Ffilter%3DcreationDate' \
                                               '%3A%282022-02-01T07%3A00%3A00.000Z..2022-03-01T06%3A59%3A59.999Z%29' \
                                               '%2CdateRangeId%3Acustom%26limit%3D50 '
                driver.get(payouturl)
                length = driver.find_element(By.XPATH, '//*[@id="transactions-list"]/div[2]/div[1]/div[2]/div')
                textlen = length.find_element(By.CSS_SELECTOR, "span").text
                if int(textlen[-2:]) > 28:
                    dropdown = driver.find_element(By.XPATH,
                                                   '//*[@id="transactions-list"]/div[2]/div[2]/div/span['
                                                   '2]/select/option[3]')
                    dropdown.click()
                time.sleep(2)

                fees, net = fees_net()

                fees_total["hurricane"] += fees["hurricane"]
                fees_total["700"] += fees["700"]
                fees_total["sunset"] += fees["sunset"]
                fees_total["washington"] += fees["washington"]

                net_total["hurricane"] += net["hurricane"]
                net_total["700"] += net["700"]
                net_total["sunset"] += net["sunset"]
                net_total["washington"] += net["washington"]

    print("\nHurricane")
    fee_total_hurricane = (fees_total["hurricane"])
    net_total_hurricane = (net_total["hurricane"])
    print("Fees: ", fee_total_hurricane, " ", "Net: ", net_total_hurricane, "\n")

    print("Sunset")
    fee_total_sunset = (fees_total["sunset"])
    net_total_sunset = (net_total["sunset"])
    print("Fees: ", fee_total_sunset, " ", "Net: ", net_total_sunset, "\n")

    print("Washington")
    fee_total_wash = (fees_total["washington"])
    net_total_wash = (net_total["washington"])
    print("Fees: ", fee_total_wash, " ", "Net: ", net_total_wash, "\n")

    print("700")
    fee_total_700 = (fees_total["700"])
    net_total_700 = (net_total["700"])
    print("Fees: ", fee_total_700, " ", "Net: ", net_total_700, "\n")

    print("**************************************************")
    print("700/Wash")
    fee_total_700_wash = (fee_total_700 + fee_total_wash)
    net_total_700_wash = (net_total_700 + net_total_wash)
    print("Fees: ", fee_total_700_wash, " ", "Net: ", net_total_700_wash, "\n")
    print("**************************************************\n")

    print("Total")
    total_fees = fee_total_700_wash + fee_total_sunset + fee_total_hurricane
    total_net_before = net_total_700_wash + net_total_sunset + net_total_hurricane
    print("Fees: ", total_fees, " ", "Net: ", total_net_before, "\n")
    print("*this does not include printed mistakes\n")

    if int(net_total_hurricane) > 0 and int(net_total_sunset) > 0 and int(net_total_700_wash) > 0:
        pie_chart(net_total_hurricane, net_total_sunset, net_total_700_wash)


def main():
    file_path = 'ebay_payouts_.txt'
    adjust_zoom()
    url = "http://www.ebay.com/"
    driver.get(url)

    input("Click and hit Double Enter\n")
    sys.stdout = open(file_path, "w")

    list_of_dicts = payout_table()
    net_fees_total(list_of_dicts)
    sys.stdout.close()
    # fees_net()


main()

# Notes
# * = hurricane
# ~ = 700
# - = sunset
# ^ = washington]


