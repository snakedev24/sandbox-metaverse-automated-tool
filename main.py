import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
import pyperclip
from datetime import datetime
import os
import re
def extract_data(url):
    data = requests.get(url).json()
    return data.get("experiences", [])
    
def get_wallet_id(driver, entry_data):
    try:
        driver.get(entry_data["Owner Link"])
        wallet_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'wallet-btn'))
        )
        if wallet_btn:
            wallet_btn.click()
            sleep(2)
            return pyperclip.paste()
        else:
            return ""
    except Exception as e:
        return "wallet_id" 


def get_owner_handle(driver, entry_data):
    try:
        driver.get(entry_data["Owner Link"])
        handle_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'name'))
        ).text.strip()
        return handle_name
    except:
        return "No handle_name"
    

def process_entry(driver, entry):
    entry_data = {
        "Experience Name": entry.get("name", "null"),
        "Size": f"{entry.get('sizeX', 'null')}x{entry.get('sizeY', 'null')}",
        "Quests": entry.get("quests", "null"),
        "Rating": entry.get("rating", "null"),
        "Plays": entry.get("visits", "null"),
        "Tags": "",
        "Playable?": "Yes" if entry.get("status", "null") == "live" else "No",
        "Coordinates": f"{entry.get('x', 'null')}, {entry.get('y', 'null')}",
        "Single/Multi?": "Multi" if entry.get("gameMode", "null") == 1 else "Single",
        "Opening Date": "",
        "Last Update": "",
        "Map Link": f"https://www.sandbox.game/en/map/?x={entry.get('x', 'null')}&y={entry.get('y', 'null')}&lng={entry.get('x', 'null')}&lat={entry.get('y', 'null')}&zoom=6",
        "Details Link": f"https://www.sandbox.game/en/experiences/{quote(entry.get('name', 'null'))}/{entry.get('experienceId', 'null')}/page",
        "Description": entry.get("description", "null"),
        "Owner Handle": '',
        "Owner Name": entry.get("Owner", {}).get("username", "null"),
        "# of LAND": "",
        "# of Estates": "",
        "# of Experiences": "",
        "Owner Link": f"https://www.sandbox.game/en/users/{entry.get('Owner', {}).get('username', 'null')}/",
        "Wallet ID": "",
        "Experience Icon": ""
    }
    entry_data["Wallet ID"] = get_wallet_id(driver, entry_data)
    entry_data["Owner Handle"] = get_owner_handle(driver, entry_data)
    tag_list = []
    tag_lists= []
    url2 = entry_data['Details Link']
    data2 = requests.get(url2)
    soup2 = BeautifulSoup(data2.text, "html.parser")
    sleep(3)
    try:
        # Directly find the figure tag with the specified class
        figure_tag = soup2.find('figure', class_="banner-preview")

        # Check if figure_tag is found and has an img tag with the 'src' attribute
        img_src = figure_tag.img.get('src', '') if figure_tag and figure_tag.img else ''
        entry_data["Experience Icon"] = f'https://www.sandbox.game{img_src}' if img_src else ''
    except Exception:
        entry_data["Experience Icon"] = ''
    

    try:
        driver.get(entry_data['Map Link'])
        container_locator4 = (By.CLASS_NAME, "header")
        wait = WebDriverWait(driver, 10)  # Reduced wait time
        container4 = wait.until(EC.visibility_of_all_elements_located((container_locator4)))
        if container4:
            sleep(3)
            html_content = driver.page_source
            soup4 = BeautifulSoup(html_content, 'html.parser')
            header_div = soup4.find('div', class_='header')
            if header_div:
                next_div = header_div.find_next('div')
                if next_div:
                    tags4 = next_div.text.strip()
                    tags4 = re.sub(r'\s+', ',', tags4)  # Replace all whitespace with a single comma
                    individual_tags1 = [tag.strip() for tag in tags4.split(',') if tag.strip()]
                    tag_lists = list(set(tag_lists).union(individual_tags1))  # Merge with existing tags and remove duplicates
                    entry_data["Tags"] = ', '.join(tag_lists)   
    except Exception as e:
        entry_data['Tags'] = ''
        print(f"An error occurred: {e}")

   

    try:
        driver.get(entry_data['Details Link'])
        container_locator = (By.CLASS_NAME, "cat-label-wrapper")
        wait = WebDriverWait(driver, 20)       
        try:
            container = wait.until(EC.presence_of_element_located(container_locator))
            sleep(5)
            html_content = driver.page_source
            soup3 = BeautifulSoup(html_content, 'html.parser')
            tags = soup3.find('section', id='info').text.strip().replace('\n', '').replace("       ",",").replace("      ",",").replace("     ",",").replace("    ",",").replace("   ",",").replace("  ",",").replace(" ,",",").replace(',,,',",").replace(',,',",")
            individual_tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
            tag_list.extend(individual_tags)
            [tag_lists.append(x) for x in tag_list if x not in tag_lists]
            entry_data["Tags"] = ', '.join(tag_lists)

            try:
                first_tag = soup3.find('section', class_="dates space-between-sections").find_next('div').find_next('span', class_='text')
                if first_tag:
                    open_date_str = str(first_tag.text).strip()
                    entry_data['Opening Date'] = open_date_str
                else:
                    entry_data['Opening Date'] = ''
            except Exception as e:
                entry_data['Opening Date'] = ''
            sleep(2)

            try:
                # Extracting last date
                last_tag = soup3.find('section', class_="dates space-between-sections").find_next('div').find_next('div').find_next('span', class_='text')
                if last_tag:
                    last_date_str = str(last_tag.text).strip()
                    entry_data['Last Update'] = last_date_str
                else:
                    entry_data['Last Update'] = ''
            except Exception as e:
                entry_data['Last Update'] = ''

        except:
            sleep(2)
            container_locator2 = (By.CLASS_NAME, "dates.space-between-sections")
            wait = WebDriverWait(driver, 20)              
            try:
                container2 = wait.until(EC.presence_of_element_located(container_locator2))
                sleep(5)
                html_content = driver.page_source
                soup3 = BeautifulSoup(html_content, 'html.parser')
                tag_list = []
                tags = soup3.find('section', id='info').text.strip().replace('\n', '').replace("       ",",").replace("      ",",").replace("     ",",").replace("    ",",").replace("   ",",").replace("  ",",").replace(" ,",",")
                tag_list.append(tags)
                [tag_lists.append(x) for x in tag_list if x not in tag_lists]
                entry_data["Tags"] = ', '.join(tag_lists)

                try:
                    first_tag = soup3.find('section', class_="dates space-between-sections").find_next('div').find_next('span', class_='text')
                    if first_tag:
                        open_date_str = str(first_tag.text).strip()
                        entry_data['Opening Date'] = open_date_str
                    else:
                        entry_data['Opening Date'] = ''
                except Exception as e:
                    entry_data['Opening Date'] = ''
                sleep(2)

                try:
                    # Extracting last date
                    last_tag = soup3.find('section', class_="dates space-between-sections").find_next('div').find_next('div').find_next('span', class_='text')
                    if last_tag:
                        last_date_str = str(last_tag.text).strip()
                        entry_data['Last Update'] = last_date_str
                    else:
                        entry_data['Last Update'] = ''
                except Exception as e:
                    entry_data['Last Update'] = ''
            except Exception as e:
                entry_data["Tags"] = "No Tag"

    except TimeoutException as e:
        # Handle the exception as needed
        entry_data["Tags"] = "No Tag"  # Or set it to any default value

    sleep(4)
    driver.get(entry_data["Owner Link"])

    try:
        exp_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="public-profile-tab-Experiences"]'))
        )
        exp_tab.click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.inventory-lists a')))
        
        # Find the inventory list for experiences
        exp_inventory_list = driver.find_element(By.CLASS_NAME, "inventory-lists")
        exp_inventory_html = exp_inventory_list.get_attribute('innerHTML')
        experience_count = sum(1 for tag in BeautifulSoup(exp_inventory_html, 'html.parser').find_all('a'))
        
        entry_data["# of Experiences"] = experience_count

    except TimeoutException:
        entry_data["# of Experiences"] = 0

        
    try:
        land_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="public-profile-tab-LAND"]'))
        )
        land_tab.click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.inventory-lists a')))
        
        # Find the inventory list for land
        land_inventory_list = driver.find_element(By.CLASS_NAME, "inventory-lists")
        land_inventory_html = land_inventory_list.get_attribute('innerHTML')
        land_count = sum(1 for tag in BeautifulSoup(land_inventory_html, 'html.parser').find_all('a',recursive=False))
        
        entry_data["# of LAND"] = land_count

    except TimeoutException:
        entry_data["# of LAND"] = 0

    try:
        estate_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="public-profile-tab-Estates"]'))
        )
        estate_tab.click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.inventory-lists a')))
        
        # Find the inventory list for estates
        estate_inventory_list = driver.find_element(By.CLASS_NAME, "inventory-lists")
        estate_inventory_html = estate_inventory_list.get_attribute('innerHTML')
        estate_count = sum(1 for tag in BeautifulSoup(estate_inventory_html, 'html.parser').find_all('a',recursive=False))
        
        entry_data["# of Estates"] = estate_count

    except TimeoutException:
        entry_data["# of Estates"] = 0


        if entry_data["Rating"] != "null":
            entry_data["Rating"] = float(entry_data["Rating"])
        if entry_data["Plays"] != "null":
            entry_data["Plays"] = int(entry_data["Plays"])

        return entry_data
import time

def main():
    headers = [
        "Experience Name",
        "Size",
        "Quests",
        "Rating",
        "Plays",
        "Tags",
        "Playable?",
        "Coordinates",
        "Single/Multi?",
        "Opening Date",
        "Last Update",
        "Map Link",
        "Details Link",
        "Description",
        "Owner Handle",
        "Owner Name",
        "# of LAND",
        "# of Estates",
        "# of Experiences",
        "Owner Link",
        "Wallet ID",
        "Experience Icon"
    ]

    entries = []
    driver = webdriver.Chrome()

    csv_file = "Sandbox_data.csv"
    excel_file = "Sandbox_data.xlsx"

    # Check if CSV file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        pd.DataFrame(columns=headers).to_csv(csv_file, index=False)

    # Check if Excel file exists, if not, create it with headers
    if not os.path.isfile(excel_file):
        pd.DataFrame(columns=headers).to_excel(excel_file, index=False)

    # Start timing
    start_time = time.time()
    for i in range(1,47):
        url = f"https://api.sandbox.game/lands/es/map-list/{i}"
        data = extract_data(url)

        for entry in data:
            entry_data = process_entry(driver, entry)
            if entry_data is None:
                continue
            entries.append(entry_data)
    
            # Append data to CSV file
            pd.DataFrame([entry_data], columns=headers).to_csv(csv_file, mode='a', header=False, index=False)

            # Append data to Excel file
            existing_data = pd.read_excel(excel_file)
            new_data = pd.DataFrame([entry_data], columns=headers)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            combined_data.to_excel(excel_file, index=False)


    driver.quit()
    df = pd.read_excel(excel_file)
    df.drop_duplicates(subset=["Details Link"], inplace=True)
    df.sort_values(by="Plays", ascending=False, inplace=True)
    df.insert(0, "Entry", range(1, len(df) + 1))
    df.to_excel(excel_file, index=False)

    # End timing
    end_time = time.time()
    runtime = end_time - start_time

    print(f"Total runtime: {runtime} seconds")

if __name__ == "__main__":
    main()
