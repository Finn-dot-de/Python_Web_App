import psycopg2
from datetime import datetime, timedelta

# Verbindung zur Postgres-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    user="ly04",
    password="password",
    database="azubis"
)

days = {
    1: "Montag",
    2: "Dienstag",
    3: "Mittwoch",
    4: "Donnerstag",
    5: "Freitag",
    6: "Samstag",
    7: "Sonntag"
}

cursor = conn.cursor()

days_to_insert = 365  

data = []
for i in range(days_to_insert):
    date_to_insert = datetime.now().date() + timedelta(days=i)
    weekday = date_to_insert.weekday() + 1  

    for employee_id in range(1, 10):  
        if weekday == 6:  
            status = 2  
        elif weekday == 7:  
            status = 0  
        else:
            status = 1 
        
        data.append((employee_id, date_to_insert, days[weekday], status))


sql = "INSERT INTO Shifts (employee_id, date, day, status) VALUES (%s, %s, %s, %s)"

cursor.executemany(sql, data)

conn.commit()

cursor.close()
conn.close()


# CREATE TABLE Shifts (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     employee_id INT,
#     date DATE,
#     status ENUM('Abwesend', 'Einsatz', 'Nicht eingetragen') DEFAULT 'Nicht eingetragen',
#     FOREIGN KEY (employee_id) REFERENCES Employees(id)
# );