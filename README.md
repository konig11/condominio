# 🏢 Condominium Management System (Django)

Welcome to the Condominium Management System!  
This project was built with Django to simplify the daily operations of a condominium, offering both **administrator** and **resident** interfaces.

---

## ✨ Features

- 🛡 **Administrator Panel**:
  - Manage residents, reservations, and financial payments.
  - Register condominium expenses.
  - Monitor payment history and financial situation.

- 🏡 **Resident Panel**:
  - Make payments independently.
  - View financial balance and payment history.
  - Reserve shared condominium areas.

- 🔒 **Authentication System**:
  - Secure login/logout system.
  - Different access levels: administrator vs resident.

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Bootstrap 5
- **Database**: MYSQL, SQLite (default Django) — easily upgradeable to PostgreSQL
- **Other tools**: Django Messages Framework (alerts and notifications)

---

## 🚀 Installation
### 1. Clone the repository
  ```bash 
git clone https://github.com/konig11/condominio.git
cd condominium-management
```
### 3. Create a virtual environment and activate it
 ```bash  
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```
### 4. Install dependencies
  ```bash 
pip install -r requirements.txt
```
### 5. Apply migrations
   ```bash
python manage.py migrate
```
### 6. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```
### 7. Run the server
```bash
python manage.py runserver
```


📸 Screenshots
![Screenshot_21-3-2025_0202_127 0 0 1](https://github.com/user-attachments/assets/e40d8ce5-67ef-49dc-9525-a0ed97cd22d7)
![Screenshot_21-3-2025_03856_127 0 0 1](https://github.com/user-attachments/assets/83a9e391-a8b4-4f54-81c7-b318d3f85722)
![Screenshot_27-3-2025_1283_127 0 0 1](https://github.com/user-attachments/assets/c85eb8ed-f2ed-47e1-8a16-df8b0cfad191)


🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is open-source and available under the MIT License.

🚀 Final Note
This project reflects my journey in backend development and system design.
Feel free to fork it, contribute, or reach out if you are interested in collaboration!

Developed with ❤️ using Django.



