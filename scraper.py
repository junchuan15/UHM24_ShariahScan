import requests
from bs4 import BeautifulSoup
from urllib.request import unquote
from contextlib import redirect_stdout
import mysql.connector

# Establish a connection to MySQL database
db_connection = mysql.connector.connect(
  host="your_host",
  user="your_username",
  password="your_password",
  database="your_database"
)
cursor = db_connection.cursor()

# Establish chrome driver and go to report site URL
driver = webdriver.Firefox()
driver.get(url)
driver.execute_script("window.stop()")

# Click submit button
driver.find_element_by_xpath("/html/body/div[3]/div/section/div/div/div[1]/form/table/tbody/tr[15]/td[2]/input[1]").click()
time.sleep(5)

all_urls = driver.find_elements_by_xpath("//a[@href]")

for url in all_urls:
    pdf_url = url.get_attribute("href")
    
    if '.pdf' in pdf_url:
        # Get PDF content
        pdf_response = requests.get(pdf_url, verify=False)
        time.sleep(5)
        
        # Extract PDF file name
        filename = unquote(pdf_response.url).split('/')[-1].replace(' ', '_')
        
        # Insert PDF content into the database
        insert_query = "INSERT INTO pdf_files (filename, content) VALUES (%s, %s)"
        pdf_data = (filename, pdf_response.content)
        
        try:
            cursor.execute(insert_query, pdf_data)
            db_connection.commit()
            print(f"PDF '{filename}' uploaded to database successfully.")
        except Exception as e:
            print(f"Failed to upload PDF '{filename}' to database:", str(e))
            db_connection.rollback()

# Close cursor and database connection
cursor.close()
db_connection.close()
