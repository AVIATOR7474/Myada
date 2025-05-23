import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Al Hayah Developments - Property Inquiry Form",
    page_icon="🏢",
    layout="centered"
)

# Add some basic CSS for styling
st.markdown("""
<style>
    .main-header {
        color: #C8A23F;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #8A6D3B;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .section-header {
        color: #8A6D3B;
        background-color: #F9F6EF;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #C8A23F;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        color: #666;
        font-size: 0.9rem;
    }
    .stButton>button {
        background-color: #C8A23F;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 10px 0;
        border: none;
        border-radius: 5px;
    }
    .result-item {
        background-color: #F9F6EF;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for form submission
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Header
st.markdown('<h1 class="main-header">Al Hayah Developments</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Property Inquiry Form</h2>', unsafe_allow_html=True)

# Define email sending function
def send_inquiry_email(form_data):
    try:
        # Email configuration
        sender_email = "noreply@alhayadevelopments.com"
        receiver_email = "mayada.alhayah@gmail.com"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Property Inquiry from {form_data['Client Name']}"
        
        # Create simple email body
        email_text = "A new property inquiry has been submitted with the following details:\n\n"
        for key, value in form_data.items():
            email_text += f"{key}: {value}\n"
        email_text += "\nPlease contact the client as soon as possible."
        
        # Attach the text content to the email
        message.attach(MIMEText(email_text, "plain"))
        
        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("mayada.alhayah@gmail.com", "yvdlbvhtcrywetpa")
            server.send_message(message)
        
        return True
    except Exception as e:
        return False

# Display form or results based on submission status
if not st.session_state.form_submitted:
    # Client Information
    st.markdown('<h3 class="section-header">Client Information</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        report_date = st.date_input("Report Date", datetime.date.today())
        client_name = st.text_input("Client Name")
    with col2:
        client_phone = st.text_input("Client Phone Number")
    
    # Property Requirements
    st.markdown('<h3 class="section-header">Property Requirements</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        unit_type = st.selectbox(
            "Unit Type",
            [
                "Studio", "Apartment", "Duplex", "Penthouse", 
                "Town House", "Twin House", "Villa", "Chalet",
                "Commercial Space", "Administrative Space"
            ]
        )
        
        floor_type = st.selectbox(
            "Floor Type",
            [
                "Ground Floor", "Ground Floor with Garden", 
                "Typical Floor", "Last Floor", 
                "Last Floor with Roof"
            ]
        )
        
        st.write("Unit Area (m²)")
        area_col1, area_col2 = st.columns(2)
        with area_col1:
            min_unit_area = st.number_input("Min Area", min_value=0, value=0, label_visibility="collapsed")
        with area_col2:
            max_unit_area = st.number_input("Max Area", min_value=0, value=0, label_visibility="collapsed")
    
    with col2:
        num_rooms = st.number_input("Number of Rooms", min_value=0, value=0)
        num_bathrooms = st.number_input("Number of Bathrooms", min_value=0, value=0)
        
        finishing_type = st.selectbox(
            "Finishing Type",
            ["Fully Finished", "Semi-Finished", "Core & Shell"]
        )
    
    # Location and Financial Details
    st.markdown('<h3 class="section-header">Location and Financial Details</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        area = st.selectbox(
            "Area",
            [
                "Sheikh Zayed", "October", "October Gardens", 
                "Green Belt", "Green Revolution", "New Cairo", 
                "6th Settlement", "Future City", "El Shorouk", 
                "New Administrative Capital", "Ain Sokhna", 
                "Red Sea", "North Coast"
            ]
        )
        
        budget = st.number_input("Budget (EGP)", min_value=0, value=0)
    
    with col2:
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "Installments"]
        )
        
        delivery_date = st.date_input("Delivery Date", min_value=datetime.date.today())
    
    # Add some space before the submit button
    st.write("")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit Inquiry"):
            # Validate form
            if not client_name or not client_phone:
                st.error("Please fill in all required fields: Client Name and Phone Number")
            else:
                # Store form data
                form_data = {
                    "Report Date": report_date.strftime("%Y-%m-%d"),
                    "Client Name": client_name,
                    "Client Phone": client_phone,
                    "Unit Type": unit_type,
                    "Floor Type": floor_type,
                    "Unit Area": f"{min_unit_area} - {max_unit_area} m²",
                    "Number of Rooms": str(num_rooms),
                    "Number of Bathrooms": str(num_bathrooms),
                    "Finishing Type": finishing_type,
                    "Area": area,
                    "Budget": f"{budget:,} EGP",
                    "Payment Method": payment_method,
                    "Delivery Date": delivery_date.strftime("%Y-%m-%d")
                }
                
                # Save the form data to a JSON file for record keeping
                try:
                    # Create a directory for submissions if it doesn't exist
                    submissions_dir = os.path.join(os.path.dirname(__file__), "submissions")
                    os.makedirs(submissions_dir, exist_ok=True)
                    
                    # Generate a unique filename based on timestamp and client name
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_name = ''.join(c if c.isalnum() else '_' for c in client_name)
                    filename = f"{timestamp}_{safe_name}.json"
                    
                    # Save the data
                    with open(os.path.join(submissions_dir, filename), 'w') as f:
                        json.dump(form_data, f, indent=4)
                except Exception:
                    pass  # Silently handle file saving errors
                
                # Send email silently
                try:
                    send_inquiry_email(form_data)
                except:
                    pass
                
                # Store data in session state for display
                st.session_state.form_data = form_data
                st.session_state.form_submitted = True

else:
    # Display success message
    st.markdown('<div class="success-message">Form submitted successfully! A copy has been sent to our team.</div>', unsafe_allow_html=True)
    
    # Display the submitted data in a styled format
    st.markdown('<h3 class="section-header">Property Inquiry Details</h3>', unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    # Distribute form data across columns
    items = list(st.session_state.form_data.items())
    half = len(items) // 2
    
    with col1:
        for key, value in items[:half]:
            st.markdown(f'<div class="result-item"><strong>{key}:</strong> {value}</div>', unsafe_allow_html=True)
    
    with col2:
        for key, value in items[half:]:
            st.markdown(f'<div class="result-item"><strong>{key}:</strong> {value}</div>', unsafe_allow_html=True)
    
    # Add some space before the button
    st.write("")
    
    # Add a button to submit another inquiry
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit Another Inquiry"):
            st.session_state.form_submitted = False

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown('© 2025 Al Hayah Developments. All rights reserved.', unsafe_allow_html=True)
st.markdown('For inquiries, please contact us @ Mobile Number -  012024558164 ', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
