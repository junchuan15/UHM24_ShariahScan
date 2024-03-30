import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
    with st.sidebar:
        selected = option_menu('Auto Shariah',
                            
                            ['Shariah Screener',
                             'Graphs & Analyses',
                             'Feedback',
                            ],
                            default_index=0)

        
    # Check if the selected option is 'Shariah Screener'
=======


    if selected == 'Shariah Screener':


        if uploaded_file is not None:
          bytes_data = uploaded_file.read()
          st.write("filename:", uploaded_file.name)

        ## with st.form("upload-form", clear_on_submit=True):
        ##  uploaded_file = st.file_uploader(model.upload_button_text_desc, accept_multiple_files=False,
        ##                                  type=['pdf'],
        ##                                  help=model.upload_help)
        ##  submitted = st.form_submit_button(model.upload_button_text)

        ##  if submitted and uploaded_file is not None:
        ##    ret = self.upload_file(uploaded_file)

          if st.button("Process", type="primary"):

            # Design table color
            headerColor = 'blue'
            rowEvenColor = 'lightblue'
            rowOddColor = 'aliceblue'

            # Design table
            fig = go.Figure(data=[go.Table(
              header=dict(
                values=['ABC Bhd','Current','Previous'],
                line_color='darkslategray',
                fill_color=headerColor,
                align=['left','center'],
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
                fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                align = ['left', 'center'],
                font = dict(color = 'darkslategray', size = 11)
                ))
              ])

            fig.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            # fig.show()
            st.write(fig)

            ## df = pd.DataFrame(np.random.randn(10, 20), columns=("col %d" % i for i in range(20)))
            ## st.dataframe(df.style.highlight_max(axis=0))

            st.markdown('**Screening Status:**')

            # non_compliant_revenue_percentage

            # Displaying the percentage
            # assume percentage = 1/2
            percentage = 1/2
            st.write("Percentage:", percentage, "%")

            if percentage <= 5:
              st.write('Congratulations! Your company is Shariah-compliant.')
            else:
              st.write('Sorry, your company did not pass the Shariah-compliant benchmark.')

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


            # Design table
            fig = go.Figure(data=[go.Table(
              header=dict(
                values=['ABC Bhd','Current','Previous'],
                line_color='darkslategray',
                fill_color=headerColor,
                align=['left','center'],
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
                fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                align = ['left', 'center'],
                font = dict(color = 'darkslategray', size = 11)
                ))
              ])

            fig.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            # fig.show()
            st.write(fig)

            ## df = pd.DataFrame(np.random.randn(10, 20), columns=("col %d" % i for i in range(20)))
            ## st.dataframe(df.style.highlight_max(axis=0))

            st.markdown('**Screening Status:**')

            # non_compliant_revenue_percentage

            # Displaying the percentage
            # assume percentage = 1/2
            percentage = 1/2
            st.write("Percentage:", percentage, "%")

            if percentage <= 5:
              st.write('Congratulations! Your company is Shariah-compliant.')
            else:
              st.write('Sorry, your company did not pass the Shariah-compliant benchmark.')

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