from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import json  # Import the json module

def clean_title(title):
    # Remove 'PreviousNext'
    title = title.replace('PreviousNext', '')
    
    # Remove 'Section X.' pattern using regex
    title = re.sub(r'Section \d+\.', '', title)
    
    # Clean up any extra spaces and strip
    return title.strip()

def scrape_page(url):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    try:
        # Load the webpage
        driver.get(url)
        # Wait for JavaScript to load
        time.sleep(1)
        
        # Parse the loaded page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the title
        section_title_element = soup.select_one('p.sectionTitle')
        if section_title_element:
            # Clean the title using our helper function
            section_title = section_title_element.get_text(strip=True)
            cleaned_title = clean_title(section_title)
            print("\nTitle:", cleaned_title)
        else:
            print("\nTitle not found.")
            cleaned_title = None
        
        # Extract the description content
        section_description_element = soup.select_one('div.panel-body')
        if section_description_element:
            section_description = section_description_element.get_text(separator="\n", strip=True)
            print("\nDescription:\n", section_description)
        else:
            print("\nDescription not found.")
            section_description = None
        
        # Find the Next link
        next_link = soup.find('a', string='Next')
        if next_link and 'href' in next_link.attrs:
            next_url = 'https://www.indiacode.nic.in' + next_link['href']
            return next_url, cleaned_title, section_description
        
        return None, cleaned_title, section_description
        
    finally:
        driver.quit()

def main():
    # Initial URL
    current_url = 'https://www.indiacode.nic.in/show-data?abv=CEN&statehandle=123456789/1362&actid=AC_CEN_5_23_00049_202346_1719552320687&sectionId=90988&sectionno=1&orderno=1&orgactid=AC_CEN_5_23_00049_202346_1719552320687'
    
    # Counter to keep track of pages (you can adjust the limit as needed)
    page_count = 1
    max_pages = 531  # Set a limit to avoid infinite loops
    
    # List to hold all titles and descriptions
    scraped_data = []
    
    while current_url and page_count <= max_pages:
        print(f"\n{'='*50}")
        print(f"Scraping page {page_count}")
        print(f"{'='*50}")
        
        # Scrape current page and get next URL
        next_url, title, description = scrape_page(current_url)
        
        # Store the title and description in the list
        if title and description:
            scraped_data.append({
                'title': title,
                'description': description
            })
        
        if next_url:
            current_url = next_url
            page_count += 1
            time.sleep(2)  # Add delay between requests
        else:
            print("\nNo more pages to scrape.")
            break
    
    # Save the scraped data to a JSON file
    with open('scraped_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)
    print("\nData saved to scraped_data.json")

if name == "main":
    main()
