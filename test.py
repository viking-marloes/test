import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openpyxl import load_workbook

# Display the logo at the top of your app
logo_url = "https://images.ctfassets.net/w2u6i2262322/6AofuFJgqbIYLaRjD6tQZs/6c98da389f59d48a8bd540f88d3f1afc/merchant_featured_1833.2661a954f317eab66ef2b67258f3644c5e7582f8.jpg?fm=webp&q=50&w=436&h=436&fit=pad"
st.image(logo_url, width=200)  # Adjust the width as needed

# Function to fetch the canonical URL
def fetch_canonical_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        canonical_tag = soup.find("link", {"rel": "canonical"})
        return canonical_tag['href'] if canonical_tag else None
    except Exception as e:
        return None

# Generate URL
def generate_url(row):
    base_url = country_base_url.get(row['country'], None)
    if base_url:
        return f"{base_url}{row['sku']}"
    else:
        return None

# Display clickable Google Sheets link for the template
google_sheet_url = "https://docs.google.com/spreadsheets/d/1JCR6q8DTQgvPtlABgnIIQe1iElCnNOAabq8MDB1aAFQ/edit?usp=sharing"
st.markdown(f'Download Template from [Google Sheet]({google_sheet_url})')
st.write("Note: Please download the template as an Excel (.xlsx) file from Google Sheets.")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])

if uploaded_file is not None:
    try:
        input_df = pd.read_excel(uploaded_file)

        # Define country_base_url with correct dictionary syntax
        country_base_url = {
        "UK": "https://www.viking-direct.co.uk/en/-p-", "uk": "https://www.viking-direct.co.uk/en/-p-", "GB": "https://www.viking-direct.co.uk/en/-p-", "gb": "https://www.viking-direct.co.uk/en/-p-",
        "IE": "https://www.vikingdirect.ie/en/-p-", "ie": "https://www.vikingdirect.ie/en/-p-",
        "DE": "https://www.viking.de/de/-p-", "de": "https://www.viking.de/de/-p-",
        "AT": "https://www.vikingdirekt.at/de/-p-", "at": "https://www.vikingdirekt.at/de/-p-",
        "NL": "https://www.vikingdirect.nl/nl/-p-", "nl": "https://www.vikingdirect.nl/nl/-p-",
        "BENL": "https://www.vikingdirect.be/nl/-p-", "benl": "https://www.vikingdirect.be/nl/-p-",
        "BEFR": "https://www.vikingdirect.be/fr/-p-", "befr": "https://www.vikingdirect.be/fr/-p-", "BEWA": "https://www.vikingdirect.be/fr/-p-", "bewa": "https://www.vikingdirect.be/fr/-p-",
        "CHDE": "https://www.vikingdirekt.ch/de/-p-", "chde": "https://www.vikingdirekt.ch/de/-p-",
        "CHFR": "https://www.vikingdirekt.ch/fr/-p-", "chfr": "https://www.vikingdirekt.ch/fr/-p-",
        "LU": "https://www.viking-direct.lu/fr/-p-", "lu": "https://www.viking-direct.lu/fr/-p-"
        }

        input_df['url'] = input_df.apply(generate_url, axis=1)

        # Fetch canonical URLs
        st.write("Fetching canonical URLs...")
        input_df['canonical_url'] = input_df['url'].apply(fetch_canonical_url)

        # Step 5: Generate output file
        output_file_name = "output-urls.xlsx"
        input_df.to_excel(output_file_name, index=False)

        # Step 6 & 7: Download the file with Streamlit
        with open(output_file_name, "rb") as file:
            st.download_button(
                label="Download output file",
                data=file,
                file_name=output_file_name,
                mime="application/vnd.ms-excel"
            )
    except Exception as e:
        st.error("An error occurred while processing the file.")
