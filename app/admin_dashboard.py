import streamlit as st
import pandas as pd
from db.database import get_db
from db.models import Booking, Customer

def admin_interface():
    st.header("Admin Dashboard")
    
    # Simple Authentication (Hardcoded for demo)
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123":
        st.success("Access Granted")
        
        db = next(get_db())
        
        # Fetch data
        bookings = db.query(Booking).all()
        
        data = []
        for b in bookings:
            data.append({
                "Booking ID": b.id,
                "Customer Name": b.customer.name,
                "Email": b.customer.email,
                "Phone": b.customer.phone,
                "Service": b.booking_type,
                "Date": b.date_time,
                "Status": b.status
            })
        
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            
            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Bookings as CSV",
                csv,
                "bookings.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            st.info("No bookings found.")
            
    elif password:
        st.error("Incorrect password")
