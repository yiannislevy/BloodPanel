# Blood Test OCR & AI Parser 🩸📄

**A full-stack application using OCR and an LLM API to automate the extraction and structured management of blood test data from PDF reports.**

---

## 🚀 Project Overview
This project automates the extraction, parsing, and structured storage of blood test results from PDF documents, providing users with an efficient dashboard to upload, analyze, and manage their medical data.

**Current features include:**

- **PDF Uploading:** Drag-and-drop functionality to upload blood test PDFs.
- **Automated OCR & Parsing:** Extracts text with `pdfplumber` and processes data with OpenAI's GPT-4o.
- **Data Validation:** Uses Pydantic to ensure accurate, structured data.
- **Database Storage:** Stores structured data using PostgreSQL and SQLAlchemy ORM.

---

## 📦 Tech Stack

### Frontend
- **React** (functional components, hooks)
- **Tailwind CSS** (planned for styling)
- **react-dropzone**

### Backend
- **FastAPI** (REST API)
- **Python**
- **OpenAI GPT-4o API**
- **pdfplumber** (OCR)
- **Pydantic** (Data validation)

### Database
- **PostgreSQL**
- **SQLAlchemy** ORM

### Development Tools
- **DBeaver** (DB Management)
- **VS Code**

---

## 🛠️ Setup & Run

### Backend
```bash
cd backend
pip3 install -r requirements.txt
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
- PDF is text based only, not scanned
- Basic functionality without frontend data management UI
- Minimal error handling
- No authentication yet

---

## 🗺️ Future Plans

### Actionable Soon 🚩
- [ ] **Frontend Dashboard:** View and manage past blood test sessions
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

## 📚 Documentation & Structure

### Project Structure
```
backend/
├── models/
│   ├── data_models.py (Pydantic models)
│   └── orm_models.py (SQLAlchemy ORM)
├── utils/
│   └── text_processors.py
├── database.py
└── main.py

frontend/
├── src/
│   ├── App.js
│   └── index.js
|   └── Upload.js
```

---

## 🔗 Quick Links
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI API](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses)
- [pdfplumber](https://github.com/jsvine/pdfplumber)

---

**Author:** [Yiannis Levy](https://github.com/yiannislevy)

---