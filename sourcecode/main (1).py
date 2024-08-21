from twilio.rest import Client

class VaccinationAppointmentSystem:
    def __init__(self, twilio_sid, twilio_auth_token, twilio_phone_number):
        self.appointments = {}
        self.reminders = {}
        self.twilio_client = Client(twilio_sid, twilio_auth_token)
        self.twilio_phone_number = twilio_phone_number

    def book_appointment(self, patient_id, date, phone_number):
        if patient_id in self.appointments:
            self.appointments[patient_id].append(date)
        else:
            self.appointments[patient_id] = [date]
        self.set_reminder(patient_id, date, phone_number)
        print(f"Appointment booked for Patient ID {patient_id} on {date}.")

    def set_reminder(self, patient_id, date, phone_number):
        reminder_message = f"Reminder: You have an appointment on {date}."
        if patient_id in self.reminders:
            self.reminders[patient_id].append(reminder_message)
        else:
            self.reminders[patient_id] = [reminder_message]

        # Send SMS
        self.send_sms(phone_number, reminder_message)

    def send_sms(self, phone_number, message):
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=phone_number
            )
            print(f"Reminder sent to {phone_number}.")
        except Exception as e:
            print(f"Failed to send SMS: {e}")

    def view_appointments(self, patient_id):
        if patient_id in self.appointments:
            print(f"Appointments for Patient ID {patient_id}:")
            for date in self.appointments[patient_id]:
                print(f"- {date}")
        else:
            print(f"No appointments found for Patient ID {patient_id}.")

    def view_reminders(self, patient_id):
        if patient_id in self.reminders:
            print(f"Reminders for Patient ID {patient_id}:")
            for reminder in self.reminders[patient_id]:
                print(f"- {reminder}")
        else:
            print(f"No reminders found for Patient ID {patient_id}.")

def main():
    # Twilio credentials (replace with your actual credentials)
    TWILIO_SID = 'your_twilio_sid'
    TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
    TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

    system = VaccinationAppointmentSystem(TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)

    while True:
        print("\nChild Vaccination Appointment System")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. View Reminders")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            patient_id = input("Enter Patient ID: ")
            date = input("Enter Appointment Date (YYYY-MM-DD): ")
            phone_number = input("Enter Phone Number (with country code +91): ")
            if not phone_number.startswith("+91"):
                print("Please enter a valid phone number with country code +91.")
                continue
            system.book_appointment(patient_id, date, phone_number)

        elif choice == '2':
            patient_id = input("Enter Patient ID: ")
            system.view_appointments(patient_id)

        elif choice == '3':
            patient_id = input("Enter Patient ID: ")
            system.view_reminders(patient_id)

        elif choice == '4':
            print("Exiting the system.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
