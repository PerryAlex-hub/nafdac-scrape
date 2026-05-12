from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_nafdac_by_nrn(nrn: str):
    """
    Scrapes the NAFDAC Greenbook for a specific NAFDAC Registration Number.
    Runs in headless mode (no visible browser) and returns all available fields.
    """
    options = Options()
    options.add_argument('--headless')  # Runs browser in the background without opening a UI window
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    all_drugs = []
    
    try:
        url = "https://greenbook.nafdac.gov.ng/"
        driver.get(url)
        
        # Wait for the page structure
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Wait for the category dropdown and Select "Drugs" (value="1")
        category_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "product_categtory"))
        )
        Select(category_dropdown).select_by_value("1")
        
        # Wait for initial data processing to finish
        time.sleep(1)
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "DataTables_Table_0_processing"))
        )
        
        # Enter the NRN to search
        search_input = driver.find_element(By.ID, "search_nrn")
        search_input.clear()
        search_input.send_keys(nrn)
        
        # Wait for search processing to finish
        time.sleep(1)
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "DataTables_Table_0_processing"))
        )

        page_num = 1
        
        while True:
            # Wait for the actual rows to appear in the table body
            rows = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@id='DataTables_Table_0']/tbody/tr"))
            )
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                
                # Check for empty state "No data available in table"
                if len(cols) == 1 and "dataTables_empty" in cols[0].get_attribute("class"):
                    break
                    
                # The DataTables typically has ~10 columns. We fetch everything available by index securely.
                if len(cols) >= 4:
                    def safe_get_text(index):
                        return cols[index].text.strip() if index < len(cols) else "N/A"

                    # Map table headers according to their DOM position
                    drug = {
                        "Product Name": safe_get_text(0),
                        "Active Ingredients": safe_get_text(1),
                        "Product Category": safe_get_text(2),
                        "NAFDAC Reg No": safe_get_text(3),
                        "Form": safe_get_text(4),
                        "Route of Administration": safe_get_text(5),
                        "Strengths": safe_get_text(6),
                        "Applicant Name": safe_get_text(7),
                        "Approval Date": safe_get_text(8),
                        "Status": safe_get_text(9),
                    }
                    all_drugs.append(drug)
            
            # Check if there is a next page
            try:
                next_btn = driver.find_element(By.ID, "DataTables_Table_0_next")
                if "disabled" in next_btn.get_attribute("class"):
                    break
                
                # Click next page via JS
                driver.execute_script("arguments[0].click();", next_btn.find_element(By.TAG_NAME, "a"))
                time.sleep(0.5) 
                
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.ID, "DataTables_Table_0_processing"))
                )
                page_num += 1
            except Exception:
                break # Break if we can't find or click pagination
                
    except Exception as e:
        print(f"Scraper Error: {e}")
    finally:
        driver.quit()
        
    return all_drugs