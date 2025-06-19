# IIIT Kota ECE 4th Semester Grades Portal

This project is a FastAPI-based web application to generate and display semester results for students of the **Electronics and Communication Engineering (ECE)** department at IIIT Kota.

### 🔧 Features

- View marksheet for each student by entering their ID
- Automatically calculates SGPA based on grades and credit weights
- Displays downloadable PDF marksheet using ReportLab
- Deployed to Hugging Face Spaces
- Case-insensitive support for student IDs (e.g., `2023KUEC2001` or `2023kuec2001`)

---

### 🌐 Usage

Visit the deployed app:  
📍 https://huggingface.co/spaces/Saumyakumar/iiitkota-sem4-ece-grades

Search result using:  
```
https://huggingface.co/spaces/Saumyakumar/iiitkota-sem4-ece-grades/api?id=2023KUEC2001
```

---

### 🗂️ Project Structure

```
project_folder/
├── app.py               # FastAPI backend
├── templates/           # Jinja2 HTML templates
├── static/              # CSS/Images like iiitkota_logo.png
├── requirements.txt     # Python dependencies
├── Dockerfile           # For Hugging Face deployment
├── .gitignore           # Excludes sensitive files
└── README.md            # This file
```

---

### 🛡️ Privacy Note

- `grades.json` is **excluded from GitHub** for student data privacy.
- You can provide a `grades_template.json` for structure reference.

---

### 🐳 Deployment (Hugging Face)

1. Add this to `.huggingface.yaml` (optional):
```yaml
sdk: docker
```
2. Push your repo (without `grades.json`) to Hugging Face Space:
```bash
git push
```

---

### 👨‍💻 Developer

Maintained by **Saumya Kumar**  
Assistant Professor, IIIT Kota  
