import sys
import datetime
import re

TM = 3
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    import xlsxwriter
except:
    print("Download Proper Library and read README.MD")
    sys.exit(1)


def get_lowest_price(prices):
    min_price = float('inf')
    lowest_price_text = None

    for p in prices:
        price_text = p.text

        # Extract dollar amount for comparison
        try:
            # Assuming the format is like "$ 9.40 (￦ 12,596)"
            dollar_part = price_text.split('$')[1].split('(')[0].strip()
            dollar_value = float(dollar_part)

            if dollar_value < min_price:
                min_price = dollar_value
                lowest_price_text = price_text
        except (IndexError, ValueError):
            # Handle cases where the price format is unexpected or conversion fails
            print(f"Could not extract a valid dollar amount from '{price_text}'.")

    print(lowest_price_text)
    return lowest_price_text if lowest_price_text else None


# Path to the WebDriver executable (provide the path to the ChromeDriver executable you downloaded)
webdriver_path = 'webdriver_path'  # change
excel_data = []
result = ["URL", "품명", "재고", "구매가", "슈퍼세일", "최저가"]

excel_data.append(result)
# Create a new instance of the Chrome browser
driver = webdriver.Chrome()

url = []
with open("ople.txt", "r") as f:
    url = f.readlines()
url = [n.strip() for n in url]


for path in url:

    driver.get(path)
    time.sleep(TM)

    stock = driver.find_elements(By.CLASS_NAME, 'text-primary')
    price = driver.find_elements(By.CLASS_NAME, 'priceArea')
    name = driver.find_elements(By.CLASS_NAME, 'itemtitle')
    detail = driver.find_elements(By.CLASS_NAME, 'detailNotice')

    lowest_price = get_lowest_price(price)

    # just for checking
    print(path)

    ifPumjol = False
    for item in detail:
        if item.text.startswith("※ 품절"):
            ifPumjol = True

    if len(detail) != 0:
        if ifPumjol:
            result = [
                path,
                name[0].text,
                "품절",
                "",
                "",
                lowest_price if lowest_price else "Price not available",
            ]
        else:
            result = [
                path,
                name[0].text,
                detail[0].text,
                "",
                "",
                lowest_price if lowest_price else "Price not available",
            ]
    else:
        result = [
            path,
            name[0].text,
            " ",
            "",
            "",
            lowest_price if lowest_price else "Price not available",
        ]

    excel_data.append(result)

driver.quit()

now = datetime.datetime.now()
nowDatetime = now.strftime(' %m-%d %H%M')
file_name = 'result_details' + nowDatetime + '.xlsx'
with xlsxwriter.Workbook(file_name) as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(excel_data):
        worksheet.write_row(row_num, 0, data)
