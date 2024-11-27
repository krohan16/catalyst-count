# **Demo Client Project**

## **Overview**
This project is a demo application designed for a client to showcase functionality for processing and managing large CSV files. It includes user authentication features and data query capabilities with custom filters.

---

## **Features**

1. **User Authentication**:
   - Login, Logout, and Sign-Up functionality.
   - Secure user session management.

2. **CSV File Processing**:
   - Upload large CSV files and process data efficiently.
   - Store and dump records into the database.
   - Support for chunk-based CSV processing to handle large files.

3. **Data Querying and Filtering**:
   - Fetch records based on user-defined custom filters.
   - Provide query counts after applying filters.

4. **Performance Optimization**:
   - Support for handling large datasets without impacting application performance.

---

## **Technology Stack**
- **Backend**: DjangoRestFramework (Python)
- **Frontend**: HTML, CSS (if applicable)
- **Database**: PostgreSQL

---

## **Setup Instructions**

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>

### Getting Started


* Git clone this repository to your local machine.
* Go to cloned directory and create **.env** at root, fill in values for all environment variables
* Create a virtual env with name **".venv"** Refer, [Virtualenv Guide](https://www.geeksforgeeks.org/python-virtual-environment/)
* Change your working directory to **backend** with following command: 

    ```cd src```
* Install required packages from "requirements.txt" with following command:
    
    ```pip install -r requirements.txt```
* Once done, Perform migrations with command: 
    
    ```python manage.py migrate``` 
    
* Then you can run your project with following command: 
    
    ```python manage.py runserver```
