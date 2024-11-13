---

# BloodBridge - Blood Donation Management System

BloodBridge is a comprehensive blood donation management system that allows users to manage blood donations, keep track of inventory, and request emergency blood donations. The project is designed for hospitals and donors, with separate dashboards and access controls for each role. It uses **React** for the frontend, **Flask** for the backend, and **MongoDB** for data storage.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Routes](#routes)
  - [Backend Routes](#backend-routes)
  - [Frontend Components](#frontend-components)
- [Usage](#usage)
- [License](#license)

---

## Project Overview

BloodBridge optimizes lifesaving resources by providing hospitals and donors with a streamlined way to manage blood requests and inventory. The system allows hospitals to submit blood requests, donors to schedule donations, and admin users to monitor the entire process.

### Features

- **Account Creation and Authentication**: Admins, hospitals, and users can register and log in.
- **Donor Management**: Allows hospitals to add and manage donor details.
- **Blood Request Management**: Hospitals can submit emergency blood requests.
- **Inventory Management**: Track the available blood inventory in real-time.
- **Event Scheduling**: Hospitals can schedule blood donation events and manage participants.

---

## Technologies Used

- **Frontend**: React.js, Axios, Tailwind CSS
- **Backend**: Flask, Flask-CORS, MongoDB
- **Database**: MongoDB
- **Authentication**: Flask-Session for managing user sessions

---

## Setup Instructions

Follow these steps to set up the project locally:

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/bloodbridge.git
   cd bloodbridge
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up MongoDB**:
   - Ensure **MongoDB** is installed and running on your machine or use a cloud-based MongoDB service like MongoDB Atlas.
   - Update the **MongoDB connection string** in the `app.py` file if necessary.
   - Make sure to have the database `bloodbridge` and the necessary collections (`users`, `requests`, `inventory`, `donors`, `events`).

6. **Run the Flask backend**:
   ```bash
   flask run
   ```
   The backend should now be running on `http://127.0.0.1:5000`.

### Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Run the React app**:
   ```bash
   npm start
   ```

   The frontend should now be running on `http://localhost:3000`.

---

## Routes

### Backend Routes

- **POST** `/api/register`: Register a new user (admin, hospital, or user).
- **POST** `/api/login`: Login a user and set session.
- **POST** `/api/logout`: Log out a user and clear the session.
- **POST** `/api/add-donor`: Add a new donor (admin or hospital only).
- **POST** `/api/emergency-request`: Submit an emergency blood request.
- **GET** `/api/pending-requests`: Get a list of pending requests (for admin).
- **GET** `/api/inventory`: Get the current blood inventory (for admin and hospitals).
- **POST** `/api/hospital-request`: Submit a blood request (hospital only).
- **GET** `/api/hospital-inventory`: Get the blood inventory for hospitals.
- **GET** `/api/hospital-request-status`: Get the status of blood requests (hospital only).
- **POST** `/api/hospital-schedule-event`: Schedule a blood donation event (hospital only).

### Frontend Components

- **Login.js**: User login form.
- **Register.js**: User registration form.
- **AddDonor.js**: Add donor details form (only accessible to admin and hospital).
- **DonorManagement.js**: Displays donor details (accessible to admin and hospitals).
- **HospitalDashboard.js**: Dashboard for hospital users to manage requests, inventory, and schedule events.
- **AdminDashboard.js**: Dashboard for admins to manage all aspects of the system.

---

## Usage

1. **Account Creation**:
   - Go to `/register` and create an account as a user, hospital, or admin.
   - Use `/login` to sign in with your account.

2. **Admin Panel**:
   - Admins can view all blood requests, update inventory, and add/manage donors.

3. **Hospital Dashboard**:
   - Hospitals can submit blood requests, manage inventory, and schedule events.

4. **User Dashboard**:
   - Users can manage their donation schedule and see their eligibility.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:

- Ensure that **MongoDB** is running and accessible.
- Make sure to handle **session management** correctly on the frontend (e.g., storing session cookies or using local storage for maintaining login state).
- The **React** frontend interacts with the **Flask backend** via API requests (using Axios).

---

