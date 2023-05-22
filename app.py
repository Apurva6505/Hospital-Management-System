from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

class Patient:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class AppointmentScheduler:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, patient, date, time):
        appointment = {
            'patient': patient,
            'datetime': datetime.datetime.combine(date, time)
        }
        self.appointments.append(appointment)

    def check_appointments(self, date):
        appointments_on_date = []
        for appointment in self.appointments:
            if appointment['datetime'].date() == date:
                appointments_on_date.append(appointment)
        return appointments_on_date

    def check_patient_appointments(self, patient):
        patient_appointments = []
        for appointment in self.appointments:
            if appointment['patient'] == patient:
                patient_appointments.append(appointment)
        return patient_appointments

# Create an instance of the AppointmentScheduler
scheduler = AppointmentScheduler()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.datetime.strptime(request.form['time'], '%H:%M').time()

        patient = Patient(name, age, gender)
        scheduler.schedule_appointment(patient, date, time)

        return render_template('success.html', name=name, date=date, time=time)

    return render_template('index.html')

@app.route('/appointments')
def appointments():
    all_appointments = scheduler.appointments
    return render_template('appointments.html', appointments=all_appointments)

if __name__ == '__main__':
    app.run(debug=True)