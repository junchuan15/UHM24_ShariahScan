import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from database import Database
from pdf_extractor import PDFExtractor
import plotly.graph_objects as go
import io
import os

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
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()

            if st.button("Process", type="primary"):
                pdf_path = f"./{uploaded_file.name}"
                pdf_extractor = PDFExtractor(pdf_path)
                company_name = pdf_extractor.extract_data_from_pdf()
                company = db.retrieve_company_data(company_name)
                if company.cash_percentage_current and company.debt_percentage_current <= 33.0:
                    company.shariah_status_current = 'Shariah Compliance'
                else:
                    company.shariah_status_current = 'Shariah Non-Compliance'

                if company.cash_percentage_previous and company.debt_percentage_previous <= 33.0:
                    company.shariah_status_previous = 'Shariah Compliance'
                else:
                    company.shariah_status_previous = 'Shariah Non-Compliance'
                    
                # Design table color
                headerColor = 'blue'
                rowEvenColor = 'lightblue'
                rowOddColor = 'aliceblue'

                # Design table
                fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=['ABC Bhd', 'Current', 'Previous'],
                        line_color='darkslategray',
                        fill_color=headerColor,
                        align=['left', 'center'],
                        font=dict(color='white', size=12)
                    ),

                    cells=dict(
                        values=[
                            ['Group Revenue', 'Group Profit/(Loss) Before Tax', 'Total Assets', 'Total Cash',
                             'Cash At Bank', 'Deposit', 'Total Debt', 'Current', 'Non-current', 'Interest Income',
                             'Dividend Income', 'Shariah Non-Compliant Activities', '<b>Benchmark Calculation</b>',
                             '<b>SCREENING STATUS</b>'],

                            # can call the readily calculated values to replace the following values
                            [1200000, 20000, 80000, 2000, 12120000],
                            [1300000, 20000, 70000, 2000, 130902000]],
                        line_color='darkslategray',

                        # 2-D list of colors for alternating rows
                        fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor] * 5],
                        align=['left', 'center'],
                        font=dict(color='darkslategray', size=11)
                    ))
                ])

                fig.update_layout(margin=dict(l=5, r=5, b=10, t=10))
                st.write(fig)
                buffer = io.BytesIO()

                # Save the figure as a pdf to the buffer
                fig.write_image(buffer, format="pdf")

                # Download the pdf from the buffer
                st.download_button(
                    label="Download PDF",
                    data=buffer.getvalue(),
                    file_name="figure.pdf",
                    mime="application/pdf",
                )

                st.markdown('**Screening Status:**')
                percentage = 1 / 2
                st.write("Percentage:", percentage, "%")

                if percentage <= 5:
                    st.write('Congratulations! Your company is Shariah-compliant.')
                else:
                    st.write('Sorry, your company did not pass the Shariah-compliant benchmark.')

                # Download button for the PDF
                st.markdown(
                    f'<a href="plotly_table.pdf" download="Shariah_Compliant_Report.pdf">Download PDF</a>',
                    unsafe_allow_html=True
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
