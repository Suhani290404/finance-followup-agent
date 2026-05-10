import streamlit as st
import pandas as pd
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Finance Credit Follow-Up Agent",
    page_icon="📧",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("📧 Finance Credit Follow-Up Email Agent")

st.markdown(
    "AI-powered system for automated invoice follow-up and escalation"
)

# ---------------- SIDEBAR ----------------

st.sidebar.header("Upload Invoice File")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

# ---------------- SAMPLE DATA ----------------

# ---------------- DATA HANDLING ----------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
# ---------------- METRICS ----------------
# ---------------- DATE PROCESSING ----------------

df["Due Date"] = pd.to_datetime(
df["Due Date"],
dayfirst=True
)

today = pd.Timestamp.today()

df["Days Overdue"] = (
today - df["Due Date"]
).dt.days

col1, col2, col3 = st.columns(3)

col1.metric("Total Invoices", len(df))

col2.metric(
"Total Outstanding",
f"₹{df['Amount'].sum():,}"
)

col3.metric(
"Critical Cases",
len(df[df["Days Overdue"] > 21])
)

st.divider()

# ---------------- TABLE ----------------

st.subheader("Pending Invoice Queue")

st.dataframe(df, use_container_width=True)

# ---------------- ESCALATION ENGINE ----------------

def get_stage(days):

if days <= 7:
    return "Stage 1 - Friendly"

elif days <= 14:
    return "Stage 2 - Firm"

elif days <= 21:
    return "Stage 3 - Serious"

elif days <= 30:
    return "Stage 4 - Urgent"

else:
    return "Escalate to Legal"

df["Follow-Up Stage"] = df["Days Overdue"].apply(get_stage)
def generate_email(client_name, invoice,
                amount, days_overdue,
                stage):

if stage == "Stage 1 - Friendly":

    return f"""
Subject: Friendly Reminder for Invoice {invoice}

Dear {client_name},

Hope you're doing well.

This is a gentle reminder regarding invoice {invoice} for ₹{amount}, which is currently {days_overdue} days overdue.

We would appreciate it if you could process the payment at your earliest convenience.

Best regards,
Finance Team
"""

elif stage == "Stage 2 - Firm":

    return f"""
Subject: Payment Reminder for Invoice {invoice}

Dear {client_name},

This is a reminder that invoice {invoice} amounting to ₹{amount} is overdue by {days_overdue} days.

Kindly arrange payment as soon as possible to avoid escalation.

Regards,
Finance Team
"""

elif stage == "Stage 3 - Serious":

    return f"""
Subject: Urgent Payment Follow-Up for Invoice {invoice}

Dear {client_name},

Invoice {invoice} for ₹{amount} remains unpaid and is now overdue by {days_overdue} days.

Please treat this matter seriously and process payment immediately.

Regards,
Finance Collections Team
"""

elif stage == "Stage 4 - Urgent":

    return f"""
Subject: Final Reminder Before Escalation

Dear {client_name},

Despite previous reminders, invoice {invoice} for ₹{amount} is overdue by {days_overdue} days.

Immediate payment action is required to avoid further escalation.

Regards,
Finance Escalation Team
"""

else:

    return f"""
Subject: Legal Escalation Notice

Dear {client_name},

Invoice {invoice} for ₹{amount} has remained unpaid for {days_overdue} days.

This matter is now being reviewed for legal escalation.

Please contact us immediately.

Regards,
Legal Collections Team
"""
st.subheader("AI Email Generator")

selected_row = st.selectbox(
"Select Client",
df.index
)

if st.button("Generate Follow-Up Email"):

row = df.loc[selected_row]

email = generate_email(
    row["Client"],
    row["Invoice"],
    row["Amount"],
    row["Days Overdue"],
    row["Follow-Up Stage"]
)

st.text_area(
    "Generated Email",
    email,
    height=300
)

# ---------------- FINAL TABLE ----------------

st.subheader("Follow-Up Classification")

st.dataframe(df, use_container_width=True)