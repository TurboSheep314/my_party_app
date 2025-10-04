# ---------- Imports ----------
import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# ---------- Google Sheets Setup ----------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
if "GOOGLE_CREDENTIALS" in st.secrets:
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
# Load local credentials file (in same folder as app.py)
#creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
client = gspread.authorize(creds)
#st.write("Accessible sheets:")
#for spreadsheet in client.openall():
#    st.write(spreadsheet.title)
#st.write("🔍 Sheets this service account can access:")
#try:
#    for s in client.openall():
#        st.write("✅", s.title)
#except Exception as e:
#    st.error(f"Error accessing sheets: {e}")
# Open the Google Sheet (must match exact sheet name)
#sheet = client.open("My_party").sheet1  # or .worksheet("Sheet1")
sheet = client.open_by_key("10nEks8FVx_hTzF3NfcuhHUvFzT4FWU9fhl0LDJr7zDg").sheet1

# ---------- Data Functions ----------
def append_row(name, donation, rsvp):
    sheet.append_row([name, donation, rsvp])

def get_data():
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# ---------- UI: Header and Description ----------
#st.set_page_config(page_title="RSVP & Donations")
#st.title("We Need You're Help to Get the Word Out ")

st.set_page_config(page_title="Jonathan Greene Fundraiser", layout="centered")
st.title("Join the Final Push for Jonathan Greene!")

st.markdown("""


We’re working hard to get the word out about Jonathan Greene, and we need your help.  
We’re raising funds for one last mailer to reach voters — and printing and postage are expensive.

👉 Every dollar counts — even $5 makes a difference and helps us get closer to our goal.

In addition, Josh Mandel is hosting a fireside chat with Jon at his home.  
This is a great opportunity to meet Jon in person and hear about his vision.  
**Suggested donation: \\$50 to \\$250.**

Let’s finish strong — thank you for standing with us!


👇 Fill out the form below and click the links to RSVP and pledge your donation.  
*The form only lets me know how effective I have been.*
""")

# ---------- RSVP & Donation Form ----------
st.subheader("RSVP & Donation Form")
with st.form("rsvp_form", clear_on_submit=True):
    name = st.text_input("Your Name", max_chars=50)
    donation = st.number_input("How much are you planning to donate?", min_value=0, step=1)
    rsvp = st.radio("Will you be attending the fireside chat?", ["Yes", "No"])
    submitted = st.form_submit_button("Submit")

    if submitted and name:
        append_row(name, donation, rsvp)
        st.success("Thank you for your response!")

# ---------- External Links ----------
st.markdown("""
👇 Use these links to donate and RSVP to Josh.
           

🔗 [RSVP Fireside Chat with Jonathan Greene](https://www.evite.com/event/017BUOV7MBWAKUYCOEPQSMXFTQJZRY?...)  
🔗 [Jonathan's Website for Donations](https://www.jonathan4newton.com)
""")

# ---------- Summary Section ----------
st.subheader("Current Summary")

try:
    data = get_data()

    total_donation = data["Donation"].sum()
    rsvp_list = data[data["RSVP"] == "Yes"]["Name"].tolist()

    st.metric("Total Committed Donations ($)", int(total_donation))

    #st.write("### People Attending:")
    #if rsvp_list:
       # for person in rsvp_list:
           # st.write(f"✅ {person}")
    #else:
        #st.write("No one has RSVP’d yet.")
except Exception as e:
    st.warning(f"Unable to load summary data: {e}")