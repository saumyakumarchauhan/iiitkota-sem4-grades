# IIIT Kota - ECE Semester 4 Grade Portal

This web application allows students from the **Electronics and Communication Engineering (ECE)** department at **IIIT Kota** (Batch 2023–2027) to view their Semester 4 grades and download their marksheet in PDF format.

🚀 Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/Saumyakumar/iiitkota-sem4-ece-grades)

---

## 📚 Features

- 🔍 Search by Student ID (case-insensitive)
- 📊 View SGPA and subject-wise grades
- 📄 Download auto-generated PDF marksheet
- 🖼️ IIIT Kota logo and styled result layout
- ⚡ Built with FastAPI, Jinja2, and ReportLab

---

## 🧑‍💻 How to Use

1. Visit the app on Hugging Face Spaces:  
   https://Saumyakumar-iiitkota-sem4-ece-grades.hf.space

2. Append your **Student ID** (e.g., `2023KUEC2001`) to the `/redirect` URL:  
   https://Saumyakumar-iiitkota-sem4-ece-grades.hf.space/redirect?id=2023kuec2001

   - ✅ Both `2023KUEC2001` and `2023kuec2001` are accepted.

3. View your grade details on the result page.

4. Click the **"Download PDF"** button to get your marksheet.

---

## 🗂️ Project Structure

```
project_folder/
├── app.py                # FastAPI backend
├── grades.json           # Student grade data
├── requirements.txt      # Python dependencies
├── Dockerfile            # Hugging Face deployment config
├── static/
│   └── iiitkota_logo.png # Institute logo
├── templates/
│   └── result.html       # Jinja2 result page
```

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **Jinja2** – Templating engine
- **ReportLab** – PDF generation
- **HTML/CSS** – Frontend styling
- **Docker** – Containerized deployment
- **Hugging Face Spaces** – Hosting platform

---

## 👨‍💼 Prepared By

**Saumya Kumar**  
Undergraduate Student, IIIT Kota  
B.Tech – Computer Science and Engineering

---

## 📜 License

This project is for educational use only. Contact the maintainer for reuse or collaboration.
