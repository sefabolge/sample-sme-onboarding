# 💼 SME Onboarding Prototype

This is a full-stack Django + React prototype simulating the onboarding flow for Small and Medium Enterprises (SMEs) onto the platform.

---

## 🎯 Project Objective

Simulate the SME onboarding process:
- Users sign up and upload documents (e.g. Certificate of Incorporation).
- Users Login to check status
- Admins review and approve, reject, or push back for re-upload.
- Stretch goal: prevent low-quality or invalid document submissions (blurry, wrong doc, etc.).

---

## 📦 Features

- Secure sign up / login with JWT (SimpleJWT)
- File upload with document type validation
- Re-upload flow for push-backed documents
- Status-based user guidance (PENDING / APPROVED / PUSHBACK / REJECTED)
- Document-specific admin pushback reasons
- Optional OCR + image sharpness validation before submission

---


### ⚙️ Backend Setup

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate # On macOS / Linux
pip install -r requirements.txt

# Setup env
copy .env.example .env  # Or create manually with DB and secret config

# Run server
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

#Tests
cd backend
pytest

# Frontend Setup
cd frontend
npm install
npm run dev  # or npm start
```
---

📌 Why Both Application.status and Document.status Are Used
We track review status at two levels:
- Application.status: Reflects the overall onboarding progress (e.g. PENDING, APPROVED, PUSHBACK, REJECTED). Used to block user progression when any issues exist across the application.
- Document.status: Tracks individual file review states (e.g. PENDING, PUSHBACK, APPROVED, REJECTED). Used to show which specific document needs re-upload and why.

This separation allows:
- Admins to push back or reject specific documents without affecting others.
- Admins to reject or pause the whole application for reasons not limited to document issues (e.g. eligibility, manual checks).
- The frontend to give users both high-level feedback (application status) and specific actions (reupload a pushed-back document).

---

⭐ Stretch Goal 

1. Local Python (OCR with Tesseract or OpenCV) - (Implemented in utils/validations.py as example)

- Using OpenCV to measure image sharpness via Laplacian variance
- Using pytesseract (Tesseract OCR) to ensure the text contains expected terms like “Certificate of Incorporation”

Image Clarity Detection
We use OpenCV to calculate the Laplacian variance — a metric that reflects how blurry an image is.
If the variance is below a certain threshold (e.g., variance < 100), we flag the document as potentially unreadable.

OCR Text Validation
We use pytesseract (Python bindings for Tesseract OCR) to extract text from uploaded files.
We then check if the extracted content includes expected terms like "Certificate of Incorporation".

This helps us automatically reject garbage or irrelevant submissions before they reach admin review.

2. Cloud OCR (Production-Grade: Azure (Form Recognizer) / AWS(Textract))

- This would allow fully automated validation + metadata extraction (e.g. incorporation date, company name).

---
