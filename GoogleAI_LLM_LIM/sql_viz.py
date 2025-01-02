from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# Define Your Prompt with Visualization Examples
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION, MARKS.

    Examples of questions and their SQL commands:
    - Example 1: How many entries of records are present? 
      SQL: SELECT COUNT(*) FROM STUDENT;

    - Example 2: Tell me all the students studying in Data Science class.
      SQL: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

    - Example 3: Plot a pie chart of the number of students in each CLASS.
      SQL: SELECT CLASS, COUNT(*) AS STUDENT_COUNT FROM STUDENT GROUP BY CLASS;

    - Example 4: Show a bar graph of average MARKS for each CLASS.
      SQL: SELECT CLASS, AVG(MARKS) AS AVERAGE_MARKS FROM STUDENT GROUP BY CLASS;

    Ensure the SQL command does not contain any extraneous formatting like '```' or 'sql' tags.
    """
]

# Streamlit App
st.set_page_config(page_title="SQL Data Visualization App")
st.header("Gemini SQL Query and Visualization App")

question = st.text_input("Enter your question: ", key="input")
submit = st.button("Ask the question")

# Visualization Function
def plot_data(df, plot_type, x_col, y_col):
    st.subheader("Data Visualization")
    fig, ax = plt.subplots()

    if plot_type == "Pie Chart":
        df.set_index(x_col)[y_col].plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    elif plot_type == "Bar Graph":
        df.plot.bar(x=x_col, y=y_col, ax=ax, legend=False)
        st.pyplot(fig)
    else:
        st.warning("Unknown plot type. Supported types are Pie Chart and Bar Graph.")

# Handle user input
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query:")
    st.code(response, language='sql')

    try:
        data = read_sql_query(response, "student.db")
        st.subheader("Query Result:")
        st.write(data)

        # Check for visualization requests
        if "plot" in question.lower():
            if "pie" in question.lower():
                if "class" in question.lower():
                    plot_data(data, "Pie Chart", x_col="CLASS", y_col="STUDENT_COUNT")
                else:
                    st.warning("The data doesn't seem suitable for a pie chart.")
            elif "bar" in question.lower():
                if "marks" in question.lower():
                    plot_data(data, "Bar Graph", x_col="CLASS", y_col="AVERAGE_MARKS")
                else:
                    st.warning("The data doesn't seem suitable for a bar graph.")
            else:
                st.warning("Please specify either 'pie chart' or 'bar graph' for visualization.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
