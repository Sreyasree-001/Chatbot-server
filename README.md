# 🧠 Chatbot Server

A backend server for an AI-powered chatbot application tailored for e-commerce platforms. This server handles user authentication, product queries, and intelligent response generation based on customer input.

## 🚀 Features

- ✅ JWT-based authentication system
- ✅ RESTful APIs for user login and registration
- ✅ Dynamic product query handling (e.g., "show me electric products")
- ✅ MySQL integration for storing and fetching product data
- ✅ Built using Flask and SQLAlchemy

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (with Docker)
- **Authentication:** JWT (JSON Web Tokens)
- **Other Libraries:** 
  - `flask_cors` for CORS handling
  - `nltk` for basic NLP processing
  - `pymongo` for database operations

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sreyasree-001/Chatbot-server.git
   cd Chatbot-server
2. Create a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
4. Configure environment variables
     Create a .env file and add your MongoDB URI and JWT secret:
     DATABASE_URL="ypur-databse-url"
      JWT_SECRET_KEY=your-secret-key
5. Run the server :
   python app.py
## 🔍 API Endpoints
| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| POST   | `/register`         | Register a new user     |
| POST   | `/login`            | Login and receive token |
| GET    | `/search-products`  | Get all products        |
| POST   | `/query`            | Smart product query     |

### 📌 Example Product Query
{
  "message": "Show me cheap kitchen appliances"
}

### 🔐 JWT Auth Example
Authorization: Bearer <your_token>

## 📁 Project Structure
![image](https://github.com/user-attachments/assets/34159d14-5f27-4e6e-92b1-43bcbb9578ab)

### 🙋‍♀️ Author
Sreyasree Sasmal
📫 sreyasree202@gmail.com

### 📄 License
This project is licensed under the MIT License.

