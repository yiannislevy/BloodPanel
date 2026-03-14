# Blood Test OCR & AI Parser 🩸📄

**A full-stack application using OCR and an LLM API to automate the extraction and structured management of blood test data from PDF files.**

---

## 🚀 Project Overview
This project automates the extraction, parsing, and structured storage of blood test results from PDF documents, providing users with an efficient dashboard to upload, analyze, and manage their medical data.

**Current features include:**

- **PDF Uploading:** Drag-and-drop functionality to upload blood test PDFs.
- **Automated OCR & Parsing:** Extracts text and formats data with OpenAI's GPT-4o.
- **Data Validation:** Uses Pydantic to ensure accurate, structured data.
- **Database Storage:** Stores structured data using PostgreSQL and SQLAlchemy ORM.

---

## 📦 Tech Stack

### Frontend
- **React** (functional components, hooks)
- **react-dropzone**

### Backend
- **Python**
- **FastAPI** (REST API)
- **Pydantic** (Data validation)
- **OpenAI GPT-4o API** (Data formatting & (Optional) OCR)
- **pdfplumber**
- **pdf2image**

### Database
- **PostgreSQL**
- **SQLAlchemy** ORM
- **Alembic**

### Development Tools
- **DBeaver** (DB Management)
- **VS Code**

---

## 🛠️ Setup & Run

### Prerequisites
- Python 3.11
- Node.js
- PostgreSQL running locally, with a database created (tables are auto-created on first run)
- An OpenAI API key

### Environment Variables
```bash
cp .env.example .env
# then fill in your OpenAI key and database credentials
```

### Backend
From the project root:
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 🚧 Current Limitations
- Minimal error handling
- No authentication(yet)

---

## 🗺️ Future Plans

### Actionable Soon 🚩
- [x] ~~**Frontend Dashboard:** View and manage past blood test sessions~~
- [ ] **Frontend Enhancement:** Add meaningful frontend (landing page, profile, dashboard)
- [ ] **Enhanced Error Handling:** Robust handling of OCR (scanned), LLM, and DB failures
- [ ] **JWT-based Authentication:** Secure user data and sessions
- [ ] **Dockerization:** Containerize frontend and backend
- [ ] **AWS Deployment:** Deploy application to AWS (ECS, S3)
- [ ] **CI/CD Pipeline:** Setup automated deployments with GitHub Actions

### Longer-Term (Abstract) 🌟
- [ ] **Fine-tuned AI Models:** Improve extraction accuracy with domain-specific fine-tuning
- [ ] **Advanced Analytics Dashboard:** Visualization & analysis of health metrics
- [ ] **Mobile Compatibility:** Responsive UI or dedicated mobile app

---