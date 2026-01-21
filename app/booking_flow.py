import re
from datetime import datetime
from dateutil import parser

class BookingFlow:
    def __init__(self):
        self.steps = ["detect", "collect_name", "collect_phone", "collect_service", "collect_date", "confirm"]
        self.current_step = "detect"
        self.booking_data = {}

    def process_message(self, message, state):
        """
        Main entry point for booking logic.
        """
        if state.get("booking_active"):
            return self.handle_active_booking(message, state)
        
        # Detect Intent
        if self.is_booking_intent(message):
            state["booking_active"] = True
            state["step"] = "collect_name"
            return "Certainly! I can help you book an appointment. May I have your full name, please?", state
        
        return None, state

    def is_booking_intent(self, message):
        keywords = ["book", "appointment", "schedule", "reservation", "visit", "consultation"]
        return any(word in message.lower() for word in keywords)

    def handle_active_booking(self, message, state):
        step = state.get("step")
        
        if step == "collect_name":
            if len(message.strip()) < 2:
                return "Please enter a valid name (at least 2 characters).", state
            state["data"]["name"] = message
            state["step"] = "collect_email"
            return f"Thank you, {message}. What is your email address?", state

        elif step == "collect_email":
            email_pattern = r"[^@]+@[^@]+\.[^@]+"
            if not re.match(email_pattern, message.strip()):
                return "That doesn't look like a valid email. Please try again (e.g., name@example.com).", state
            state["data"]["email"] = message
            state["step"] = "collect_phone"
            return "Got it. What is your phone number?", state

        elif step == "collect_phone":
            # Allow digits, spaces, dashes, plus sign
            if not any(char.isdigit() for char in message):
                return "Please enter a valid phone number containing digits.", state
            state["data"]["phone"] = message
            state["step"] = "collect_service"
            return "Got it. What service do you need? (e.g., Checkup, Cleaning, Root Canal)", state
        
        elif step == "collect_service":
            if len(message.strip()) < 2:
                return "Please specify a service.", state
        
        elif step == "collect_date":
            try:
                # Loose parsing for demo purposes
                state["data"]["date"] = message
                # Real implementation would parse datetime here
                # dt = parser.parse(message)
                # state["data"]["date_obj"] = dt
            except:
                pass
            
            state["step"] = "confirm"
            summary = (
                f"Please confirm your details:\n"
                f"Name: {state['data']['name']}\n"
                f"Email: {state['data']['email']}\n"
                f"Phone: {state['data']['phone']}\n"
                f"Service: {state['data']['service']}\n"
                f"Date: {state['data']['date']}\n\n"
                f"Type 'yes' to confirm or 'cancel' to stop."
            )
            return summary, state

        elif step == "confirm":
            if "yes" in message.lower():
                # Finalize booking
                state["booking_active"] = False
                state["step"] = "detect"
                return "CONFIRMED", state # Special signal to app.py to save to DB
            elif "cancel" in message.lower():
                state["booking_active"] = False
                state["data"] = {}
                return "Booking cancelled.", state
            else:
                return "Please type 'yes' to confirm or 'cancel'.", state
        
        return "Something went wrong.", state
