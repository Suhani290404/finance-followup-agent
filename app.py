import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Finance Credit Follow-Up Agent",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Finance Credit Follow-Up Email Agent")

st.markdown(
    "AI-powered system for automated invoice follow-up and escalation"
)

st.sidebar.header("Upload Invoice File")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Due Date"] = pd.to_datetime(
        df["Due Date"],
        dayfirst=True
    )

    today = pd.Timestamp.today()

    df["Days Overdue"] = (
        today - df["Due Date"]
    ).dt.days

    def get_stage(days):

        if days <= 7:
            return "Friendly"

        elif days <= 14:
            return "Firm"

        elif days <= 21:
            return "Serious"

        elif days <= 30:
            return "Urgent"

        else:
            return "Legal"

    df["Follow-Up Stage"] = df["Days Overdue"].apply(get_stage)

    st.subheader("Invoice Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Invoices",
        len(df)
    )

    col2.metric(
        "Outstanding Amount",
        f"₹{df['Amount'].sum():,.0f}"
    )

    col3.metric(
        "Critical Cases",
        len(df[df["Days Overdue"] > 21])
    )

    st.divider()

    st.subheader("Invoice Table")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Generate Follow-Up Email")

    selected_index = st.selectbox(
        "Select Invoice",
        df.index
    )

    row = df.loc[selected_index]

    if st.button("Generate Email"):

        email = f"""
Subject: Payment Follow-Up - Invoice {row['Invoice']}

Dear {row['Client']},

This is regarding invoice {row['Invoice']} amounting to ₹{row['Amount']}.

The payment is currently overdue by {row['Days Overdue']} days.

Current escalation level: {row['Follow-Up Stage']}.

Kindly process the payment at the earliest.

Regards,
Finance Team
"""

        st.text_area(
            "Generated Email",
            email,
            height=300
        )