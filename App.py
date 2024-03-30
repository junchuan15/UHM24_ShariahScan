import streamlit as st
from streamlit_option_menu import option_menu
from database import Database
from pdf_extractor import PDFExtractor
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import io
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Automating Shariah Compliant Assessment")
st.header('Automating Shariah Compliant Assessment')
st.caption("A site specially for you to review if your company is Shariah-compliant.")

# to set background color style
st.markdown(
    """
    <style>
    .main {
    background-color:Dark Gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def run_website():
    db = Database()
    with st.sidebar:
        selected = option_menu('Auto Shariah',
                            
                            ['Shariah Screener',
                             'Graphs & Analyses',
                             'Feedback',
                            ],
                            default_index=0)

    if selected == 'Shariah Screener':
       # uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
       # if uploaded_file is not None:
    #  bytes_data = uploaded_file.read()

      #  if st.button("Process", type="primary"):
       #         pdf_path = f"./{uploaded_file.name}"
        #        pdf_extractor = PDFExtractor(pdf_path)
         #       company_name = pdf_extractor.extract_data_from_pdf()             
                company = db.retrieve_company_data('HAP SENG CONSOLIDATED BERHAD')  # Assuming only one company is retrieved
                principal_activities, principal_values = db.get_principal_activity(company.name)
                st.markdown("<h2>Select Non-Shariah activities:</h2>", unsafe_allow_html=True)
                selected_values = []
                for activity, value in zip(principal_activities, principal_values):
                    checkbox = st.checkbox(f"{activity}: {value}")
                    if checkbox:
                        # Add the selected value to the list
                        selected_values.append(value)
                
                # Confirm button
                if st.button("Confirm"):
                    # Calculate total sum of selected values
                    total_selected = sum(selected_values)
                    st.write(f"Total Non-Shariah Activity: {total_selected}")
                    
                    if company.II_current >= 0:
                        interest_rate_current = round(company.II_current / company.TA_current, 2)
                    else:
                        interest_rate_current = 0

                    if company.II_previous >= 0:
                        interest_rate_previous = round(company.II_previous / company.TA_previous, 2)
                    else:
                        interest_rate_previous = 0

                    if company.cash_percentage_current <= 33.0 and company.debt_percentage_current <= 33.0:
                        company.shariah_status_current = 'Shariah Compliance'
                    else:
                        company.shariah_status_current = 'Shariah Non-Compliance'

                    if company.cash_percentage_previous <= 33.0 and company.debt_percentage_previous <= 33.0:
                        company.shariah_status_previous = 'Shariah Compliance'
                    else:
                        company.shariah_status_previous = 'Shariah Non-Compliance'

                    cell_values = [
                        ['<b>Company Name</b>', '',  company.name, '', '', '', '', ''],
                        ['<b>Financial Year End</b>', '',  company.FE_Date, '', '', '', '', ''],
                    ]

                    # Find the index of the "Principal Activities" row
                    principal_activities_index = next((i for i, sublist in enumerate(cell_values) if '<b>Principal Activities</b>' in sublist), None)

                    # Insert the "Principal Activities" row if it doesn't exist
                    if principal_activities_index is None:
                        # Assuming the first activity is stored in the variable `first_activity`
                        first_activity = principal_activities[0] if principal_activities else ''
                        cell_values.append(['<b>Principal Activities</b>', '', first_activity, '', '', '', '', ''])
                        principal_activities_index = len(cell_values) - 1

                    # Append principal activities to cell_values
                    if len(principal_activities) > 1:
                        for activity in principal_activities[1:]:  # Skip the first activity since it's already in the table
                            cell_values.insert(principal_activities_index + 1, ['','','',f"{activity}", '', '', '', ''])
                            principal_activities_index += 1

                    # Continue with the rest of the cell_values
                    cell_values.extend([
                        ['<b>Financial Parameters</b>', '', '', '<b>Current Year</b>', '', '', '<b>Previous Year</b>', '', ''],
                        ['<b>Group Revenue</b>', '', '', company.Revenue_current, '', '', company.Revenue_previous],
                        ['<b>Group Profit/(Loss) Before Tax</b>', '', '', company.PL_Before_Tax_current, '', '', company.PL_Before_Tax_previous],
                        ['<b>Total Assets</b>', '', '', company.TA_current, '', '', company.TA_previous],
                        ['<b>Total Cash</b>', '', '', company.CBB_current, '', '', company.CBB_previous],
                        ['<b>Current Debt</b>', '', '', company.current_BB_current, '', '', company.current_BB_previous],
                        ['<b>Non-Current Debt</b>', '', '', company.Noncurrent_BB_current, '', '', company.Noncurrent_BB_previous],
                        ['<b>Total Debt</b>', '', '', company.total_BB_current, '', '', company.total_BB_previous],
                        ['<b>Interest Income</b>', '', '', f"{company.II_current} ({interest_rate_current}%)", '', '', f"{company.II_previous} ({interest_rate_previous}%)"],
                        ['<b>Shariah Non-Compliant Activities</b>', '', ''],
                        [],
                        ['<b>Cash over total assets</b>', '', '', str(company.cash_percentage_current) + '%', '', '', str(company.cash_percentage_previous) + '%'],
                        ['<b>Debt over total assets</b>', '', '', str(company.debt_percentage_current) + '%', '', '', str(company.debt_percentage_previous) + '%'],
                        [],
                        ['<b>Benchmark Calculation</b>', '', '', ''],
                        ['<b>SCREENING STATUS</b>', '', '', company.shariah_status_current, '', '', company.shariah_status_previous]
                    ])

                    html_table = "<table style='border-collapse: collapse; width: 100%;'>"

                    for row in cell_values:
                        html_table += "<tr>"
                        colspan_index = 0
                        for i, cell in enumerate(row):
                            if cell == '':
                                if i > 0 and row[i - 1] != '':
                                    colspan_index = i - 1
                                    html_table += f"<td style='border: 1px solid black; padding: 12px; font-size: 14px;'>{cell}</td>"
                            else:
                                if i == colspan_index + 1:
                                    continue
                                html_table += f"<td style='border: 1px solid black; padding: 5px;'>{cell}</td>"
                        html_table += "</tr>"
                    html_table += "</table>"

                    fig = ff.create_table(cell_values)
                    st.write(fig)
                    buffer = io.BytesIO()

                    fig.write_image(buffer, format="pdf")
                    st.download_button(
                        label="Download PDF",
                        data=buffer.getvalue(),
                        file_name = f"{company.name}_Screening_Report.pdf",
                        mime="application/pdf",
                    )

            # Check if the selected option is 'Graphs & Analyses'
    if selected == 'Graphs & Analyses':
                st.write("Here are some analyses and graphs.")

            # Check if the selected option is 'Feedback'
    if selected == 'Feedback':
                st.write("We provide a safe scape for our end-users to express your feelings about the website.")
                st.write("We kindly ask for your feedback for our future improvement.")
                feedback = st.text_input('Your feedback:', ' ')
                upload_media = st.file_uploader("Please upload if you have any proof or picture:", type="jpg")
                if st.button("Submit", type="primary") and feedback is not None:
                    st.write("Your feedback is saved. Thank you!")


run_website()

        
