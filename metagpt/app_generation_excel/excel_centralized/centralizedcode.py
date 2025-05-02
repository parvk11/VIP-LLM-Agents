## main.py

import streamlit as st
import pandas as pd

class ExcelDataProcessor:
    def __init__(self):
        self.uploaded_file = None

    def main(self):
        self.upload_file()
        self.display_content()

    def upload_file(self):
        self.uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    def display_content(self):
        if self.uploaded_file is not None:
            data = pd.read_excel(self.uploaded_file)
            st.dataframe(data)

if __name__ == "__main__":
    processor = ExcelDataProcessor()
    processor.main()
