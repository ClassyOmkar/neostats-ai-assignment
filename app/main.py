import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app.config as config
from db.database import init_db, get_db
from db.models import Customer, Booking
from app.rag_pipeline import process_pdf, create_vector_store, get_rag_response
from app.booking_flow import BookingFlow
from app.admin_dashboard import admin_interface
from utils.email_service import send_confirmation_email

# Initialize Database
init_db()

def main():
    st.set_page_config(
        page_title="Dental Clinic Booking Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Dental Clinic Booking Assistant")

    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "booking_flow" not in st.session_state:
        st.session_state.booking_flow = BookingFlow()
    if "booking_state" not in st.session_state:
        st.session_state.booking_state = {
            "booking_active": False,
            "step": "detect",
            "data": {}
        }
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    # Sidebar for Navigation & Upload
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to", ["Chat", "Admin Dashboard"])
        
        st.divider()
        st.header("Knowledge Base")
        uploaded_files = st.file_uploader(
            "Upload Clinic Information (PDF)", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("Process PDFs"):
            with st.spinner("Processing documents..."):
                text = process_pdf(uploaded_files)
                vs = create_vector_store(text)
                if vs:
                    st.session_state.vector_store = vs
                    st.success("Documents processed successfully!")
                else:
                    st.error("No extractable text found in documents.")

    if page == "Chat":
        chat_interface()
    elif page == "Admin Dashboard":
        admin_interface()

def chat_interface():
    st.subheader("Patient Support & Booking")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("How can I help you today?"):
        # User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant Response Logic
        response = ""
        
        # 1. Process Booking Flow
        booking_resp, updated_state = st.session_state.booking_flow.process_message(
            prompt, 
            st.session_state.booking_state
        )
        st.session_state.booking_state = updated_state
        
        if booking_resp:
            if booking_resp == "CONFIRMED":
                # Save to DB
                save_booking(st.session_state.booking_state["data"])
                # Send Email
                email_sent, email_msg = send_confirmation_email(
                    st.session_state.booking_state["data"]["email"],
                    st.session_state.booking_state["data"]
                )
                
                response = f"✅ Your appointment has been confirmed! An email confirmation has been sent to {st.session_state.booking_state['data']['email']}."
                if not email_sent:
                    response += f"\n(Note: Email sending failed: {email_msg})"
            else:
                response = booking_resp
                
        # 2. RAG / General Chat if not booking
        else:
            if st.session_state.vector_store:
                response = get_rag_response(prompt, st.session_state.vector_store)
            else:
                # Fallback to simple intent detection or request for upload
                response = "I can help you with bookings. Please upload our brochure for specific questions, or just ask to 'book an appointment'."

        # Display Assistant Message
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def save_booking(data):
    """Saves the completed booking to the database."""
    db = next(get_db())
    
    # Create/Find Customer
    customer = db.query(Customer).filter(Customer.email == data['email']).first()
    if not customer:
        customer = Customer(
            name=data['name'], 
            email=data['email'], 
            phone=data['phone']
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    
    # Create Booking
    # Note: Parsing date properly is skipped for robustness in demo, storing as string/datetime
    from datetime import datetime
    try:
        booking_date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M") # Expected format
    except:
        booking_date = datetime.utcnow() # Fallback for demo
        
    booking = Booking(
        customer_id=customer.id,
        booking_type=data['service'],
        date_time=booking_date,
        status="Confirmed"
    )
    db.add(booking)
    db.commit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please refresh the page or try again later.")
        print(f"CRITICAL ERROR: {e}")
