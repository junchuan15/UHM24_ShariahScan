import streamlit as st 
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Automating Shariah Compliant Assessment")

def run_website():
    with st.sidebar:
        selected = option_menu('Auto Shariah',
                            
                            ['Shariah Screener',
                             'Some Graph idk',
                             'Some Analysis idk',
                            ],
                            default_index=0)
        
    # Check if the selected option is 'Analytics Dashboard'
    if selected == 'Shariah Screener':
        # Add a file uploader button
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")



run_website()



        
