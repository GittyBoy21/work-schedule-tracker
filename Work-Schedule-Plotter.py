import streamlit as st
import pandas as pd
import datetime
import calendar
from matplotlib import pyplot as plt

# App title
st.title("Work Schedule & Income Tracker")

# Select workdays using a date picker
st.sidebar.header("Step 1: Select Workdays")
workdays = st.sidebar.date_input(
    "Pick your workdays for 2025 (multiple allowed):",
    [],
    min_value=datetime.date(2024, 12, 1),
    max_value=datetime.date(2025, 12, 31),
    key="workdays"
)

# Set income goal per day
st.sidebar.header("Step 2: Set Your Income Goal")
income_goal = st.sidebar.slider(
    "Daily income goal ($):", 0, 400, 200, step=10
)

# Enter actual income earned for workdays
st.sidebar.header("Step 3: Enter Actual Income Earned")
actual_income = {}
if workdays:
    for day in workdays:
        actual_income[day] = st.sidebar.number_input(
            f"Income earned on {day.strftime('%b %d, %Y')}:",
            min_value=0,
            max_value=400,
            value=income_goal,
            step=10
        )

# Organize data into a DataFrame
if workdays:
    df = pd.DataFrame({
        "Date": pd.to_datetime(workdays),
        "Income Goal": [income_goal] * len(workdays),
        "Actual Income": [actual_income[day] for day in workdays]
    })
    df["Day"] = df["Date"].dt.day_name()
    df["Difference"] = df["Actual Income"] - df["Income Goal"]

    st.subheader("Workday Data")
    st.write(df)

    # Total income summary
    total_income = df["Actual Income"].sum()
    goal_income = len(workdays) * income_goal
    st.subheader("Income Summary")
    st.write(f"Total Income Earned: ${total_income:.2f}")
    st.write(f"Total Income Goal: ${goal_income:.2f}")
    st.write(f"Difference: ${total_income - goal_income:.2f}")

    # Plot income vs goal
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Actual Income"], label="Actual Income", marker='o')
    ax.axhline(y=income_goal, color='r', linestyle='--', label="Income Goal")
    ax.set_xlabel("Date")
    ax.set_ylabel("Income ($)")
    ax.set_title("Income vs Goal")
    ax.legend()
    st.pyplot(fig)

# Download data to Google Sheets
st.sidebar.header("Step 4: Export Your Data")
if st.sidebar.button("Export to Google Sheet"):
    # Placeholder for Google Sheets integration
    st.sidebar.warning("Google Sheets integration is not implemented yet.")
    # For now, allow downloading as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="work_schedule_2025.csv",
        mime="text/csv",
    )

# Placeholder for interactivity and flexibility
st.info("Use the sidebar to adjust workdays, income goals, and actual earnings. Future enhancements include direct Google Sheets integration.")
