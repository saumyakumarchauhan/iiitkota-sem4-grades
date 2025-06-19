import tempfile
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


GRADE_POINTS = {
    "AA": 10, "AB": 9, "BB": 8, "BC": 7,
    "CC": 6, "CD": 5, "DD": 4, "FP": 0
}

CREDITS = {
    "CST202": 3, "ECT202": 3, "ECT204": 3, "ECT206": 3, "ECT208": 4, "ECT210": 4,
    "CSP202": 1, "ECP202": 1, "ECP204": 1, "ECP206": 1, "OTP202": 2
}

TOTAL_CREDITS = sum(CREDITS.values())

def load_data():
    path = os.path.join(os.path.dirname(__file__), "grades.json")
    with open(path) as f:
        return json.load(f)

def calculate_sgpa(grades):
    total_points = 0
    for subject, grade in grades.items():
        point = GRADE_POINTS.get(grade, 0)
        credit = CREDITS.get(subject, 0)
        total_points += point * credit
    sgpa = total_points / TOTAL_CREDITS
    return round(sgpa, 2)

def get_rankings(data):
    student_sgpas = []
    for student in data:
        sgpa = calculate_sgpa(student["grades"])
        student_sgpas.append((student["id"], student["name"], sgpa))
    sorted_students = sorted(student_sgpas, key=lambda x: x[2], reverse=True)
    rankings = {student[0]: rank + 1 for rank, student in enumerate(sorted_students)}
    return rankings, sorted_students

def generate_pdf(id, name, grades, sgpa, rank, sorted_students):
    filename = os.path.join(tempfile.gettempdir(), f"{id}_grades.pdf")

    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=30, bottomMargin=40, leftMargin=40, rightMargin=40)
    elements = []

    styles = getSampleStyleSheet()
    centered = ParagraphStyle(name="CenteredTitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=12)

    logo_path = os.path.join(os.path.dirname(__file__), "static", "iiitkota_logo.png")
    header_table = Table([[Image(logo_path, width=1.2 * inch, height=1.2 * inch),

        Paragraph("""<para align='center'>
        <font size=18><b>Indian Institute of Information Technology, Kota</b></font><br/>
        <font size=14><b>Department of Electronics and Communication Engineering</b></font><br/>
        <font size=12><i>4th Semester Marksheet – Batch 2023–2027</i></font>
        </para>""", centered)
    ]], colWidths=[100, 440])

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('LINEBELOW', (0, 0), (-1, -1), 1.2, colors.HexColor("#004080")),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    student_info_style = ParagraphStyle(name="StudentInfo", fontSize=11, leading=16, leftIndent=12, spaceAfter=8,
                                        textColor=colors.HexColor("#333333"), alignment=TA_LEFT)

    elements.append(Paragraph(f"<b>Student ID:</b> {id}", student_info_style))
    elements.append(Paragraph(f"<b>Student Name:</b> {name}", student_info_style))
    elements.append(Paragraph(f"<b>Date of Issue:</b> {datetime.today().strftime('%d-%m-%Y')}", student_info_style))
    elements.append(Spacer(1, 20))

    data = [["Subject Code", "Grade"]]
    for subject, grade in grades.items():
        data.append([subject, grade or ""])

    grades_table = Table(data, colWidths=[200, 100])
    grades_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(grades_table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>SGPA:</b> {sgpa}", styles["Normal"]))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('<para alignment="right"><b>Prepared by: Saumya Chauhan</b></para>', styles["Normal"]))
    doc.build(elements)
    return filename

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/redirect")
def redirect_to_result(id: str):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/api?id={id.upper()}")

@app.get("/api", response_class=HTMLResponse)
def get_student_page(request: Request, id: str):
    id = id.upper()  # Normalize the ID to uppercase
    data = load_data()
    student = next((s for s in data if s["id"] == id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student ID not found")
    
    sgpa = calculate_sgpa(student["grades"])
    rankings, sorted_students = get_rankings(data)
    rank = rankings.get(id, "N/A")
    generate_pdf(id, student.get("name", "N/A"), student["grades"], sgpa, rank, sorted_students)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "id": id,
        "name": student["name"],
        "grades": student["grades"],
        "sgpa": sgpa,
        "date_of_issue": datetime.today().strftime("%d-%m-%Y")
    })


@app.get("/download")
def download_pdf(id: str):
    filepath = os.path.join(tempfile.gettempdir(), f"{id}_grades.pdf")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="PDF not found. Please generate it first.")
    return FileResponse(filepath, media_type="application/pdf", filename=f"{id}_grades.pdf")
