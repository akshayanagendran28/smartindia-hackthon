# -*- coding: utf-8 -*-
"""
Synthetic Test Document Generator
Creates 100% synthetic, fictitious demo documents (Images and text manifests)
for all Business, Self-Employment, and Education document types for SIH 2026 jury testing.
"""
import os
from PIL import Image, ImageDraw, ImageFont

class SyntheticDocumentGenerator:

    @classmethod
    def generate_all_samples(cls, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        samples = [
            ("docAadhaar", "sample_synthetic_aadhaar.png", cls._create_aadhaar_image, cls._get_aadhaar_text),
            ("docPan", "sample_synthetic_pan.png", cls._create_pan_image, cls._get_pan_text),
            ("docCaste", "sample_synthetic_caste.png", cls._create_caste_image, cls._get_caste_text),
            ("docIncome", "sample_synthetic_income.png", cls._create_income_image, cls._get_income_text),
            ("docDpr", "sample_synthetic_dpr.png", cls._create_dpr_image, cls._get_dpr_text),
            ("docUdyam", "sample_synthetic_udyam.png", cls._create_udyam_image, cls._get_udyam_text),
            ("doc10th", "sample_synthetic_10th_marksheet.png", cls._create_10th_image, cls._get_10th_text),
            ("doc12th", "sample_synthetic_12th_marksheet.png", cls._create_12th_image, cls._get_12th_text),
            ("docAdmission", "sample_synthetic_admission_letter.png", cls._create_admission_image, cls._get_admission_text),
            ("docFeeStructure", "sample_synthetic_fee_structure.png", cls._create_fee_structure_image, cls._get_fee_structure_text)
        ]

        generated_list = []
        for doc_key, filename, img_func, text_func in samples:
            img_path = os.path.join(output_dir, filename)
            txt_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")

            img = img_func()
            img.save(img_path)

            raw_txt = text_func()
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_txt)

            generated_list.append({
                "document_type": doc_key,
                "file_name": filename,
                "file_path": img_path,
                "text_path": txt_path,
                "sample_text": raw_txt[:120] + "..."
            })
        return generated_list

    @staticmethod
    def _create_aadhaar_image() -> Image.Image:
        img = Image.new("RGB", (650, 400), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (650, 8)], fill="#FF9933")
        draw.rectangle([(0, 392), (650, 400)], fill="#138808")
        draw.rectangle([(10, 10), (640, 390)], outline="#2B6CB0", width=2)
        draw.text((180, 25), "भारत सरकार / Government of India", fill="#1A365D")
        draw.text((130, 45), "भारतीय विशिष्ट पहचान प्राधिकरण (UIDAI)", fill="#2D3748")
        draw.rectangle([(40, 90), (160, 240)], outline="#4A5568", width=2, fill="#EDF2F7")
        draw.text((60, 150), "[PHOTO]", fill="#718096")
        draw.text((190, 100), "नाम / Name: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((190, 135), "जन्म तिथि / DOB: 15/08/1995", fill="#1A202C")
        draw.text((190, 170), "लिंग / Gender: पुरुष / Male", fill="#1A202C")
        draw.text((160, 280), "2345 6789 1238", fill="#C53030")
        draw.text((190, 320), "मेरा आधार, मेरी पहचान", fill="#2C5282")
        draw.text((450, 350), "[SYNTHETIC SAMPLE]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_aadhaar_text() -> str:
        return (
            "Government of India\n"
            "Unique Identification Authority of India\n"
            "Name: Aarav Rajesh Sharma\n"
            "DOB: 15/08/1995\n"
            "Gender: Male\n"
            "2345 6789 1238\n"
            "Mera Aadhaar, Meri Pehchan\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_pan_image() -> Image.Image:
        img = Image.new("RGB", (650, 400), color=(235, 248, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(10, 10), (640, 390)], outline="#2B6CB0", width=3)
        draw.rectangle([(20, 20), (630, 60)], fill="#3182CE")
        draw.text((180, 25), "INCOME TAX DEPARTMENT", fill="#FFFFFF")
        draw.text((220, 42), "GOVT. OF INDIA", fill="#EBF8FF")
        draw.text((40, 90), "Permanent Account Number / PAN Card", fill="#2C5282")
        draw.text((40, 130), "ABCPS1234F", fill="#2B6CB0")
        draw.text((40, 180), "Name: AARAV RAJESH SHARMA", fill="#1A202C")
        draw.text((40, 220), "Father's Name: RAJESH SHARMA", fill="#1A202C")
        draw.text((40, 260), "Date of Birth: 15/08/1995", fill="#1A202C")
        draw.text((450, 350), "[SYNTHETIC SAMPLE]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_pan_text() -> str:
        return (
            "INCOME TAX DEPARTMENT\n"
            "GOVT. OF INDIA\n"
            "Permanent Account Number Card\n"
            "ABCPS1234F\n"
            "Name: AARAV RAJESH SHARMA\n"
            "Father's Name: RAJESH SHARMA\n"
            "DOB: 15/08/1995\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_caste_image() -> Image.Image:
        img = Image.new("RGB", (650, 450), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 435)], outline="#2C5282", width=2)
        draw.text((170, 25), "GOVERNMENT OF MAHARASHTRA", fill="#1A365D")
        draw.text((200, 50), "OFFICE OF THE SUB-DIVISIONAL OFFICER", fill="#718096")
        draw.text((180, 75), "COMMUNITY / CASTE CERTIFICATE", fill="#2B6CB0")
        draw.text((40, 120), "Certificate No: CC/MH/2024/09876", fill="#2D3748")
        draw.text((40, 155), "This is to certify that Shri Aarav Rajesh Sharma son of Rajesh Sharma,", fill="#1A202C")
        draw.text((40, 185), "residing at Mumbai, Maharashtra, belongs to the 'Mahar' Caste,", fill="#1A202C")
        draw.text((40, 215), "which is recognized as a Scheduled Caste (SC) under the Constitution Order.", fill="#1A202C")
        draw.text((40, 270), "Issuing Authority: Sub-Divisional Officer, Mumbai", fill="#2D3748")
        draw.text((40, 300), "Date of Issue: 12/04/2024", fill="#2D3748")
        draw.text((40, 400), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_caste_text() -> str:
        return (
            "Government of Maharashtra\n"
            "Sub-Divisional Magistrate Office\n"
            "Certificate No: CC/MH/2024/09876\n"
            "This is to certify that Shri Aarav Rajesh Sharma belongs to Scheduled Caste (SC) Mahar category.\n"
            "State: Maharashtra\n"
            "Date of Issue: 12/04/2024\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_income_image() -> Image.Image:
        img = Image.new("RGB", (650, 420), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 405)], outline="#276749", width=2)
        draw.text((180, 25), "GOVERNMENT OF MAHARASHTRA", fill="#22543D")
        draw.text((220, 50), "REVENUE DEPARTMENT", fill="#718096")
        draw.text((200, 75), "ANNUAL INCOME CERTIFICATE", fill="#276749")
        draw.text((40, 120), "Certificate No: INC/MH/2024/54321", fill="#2D3748")
        draw.text((40, 160), "This is to certify that the total annual family income from all sources of", fill="#1A202C")
        draw.text((40, 190), "Aarav Rajesh Sharma, resident of Mumbai, Maharashtra,", fill="#1A202C")
        draw.text((40, 220), "is Rs. 1,80,000 (Rupees One Lakh Eighty Thousand Only) per annum.", fill="#22543D")
        draw.text((40, 270), "Issuing Authority: Tahsildar / Revenue Officer", fill="#2D3748")
        draw.text((40, 300), "Date of Issue: 15/05/2024", fill="#2D3748")
        draw.text((40, 370), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_income_text() -> str:
        return (
            "Government of Maharashtra\n"
            "Revenue Department - Tahsildar Office\n"
            "Certificate No: INC/MH/2024/54321\n"
            "This is to certify that the Annual Family Income of Shri Aarav Rajesh Sharma "
            "from all sources is assessed as Rs. 1,80,000 (Rupees One Lakh Eighty Thousand Only) per annum.\n"
            "Issuing Authority: Tahsildar\n"
            "Date: 15/05/2024\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_dpr_image() -> Image.Image:
        img = Image.new("RGB", (650, 520), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 505)], outline="#2B6CB0", width=2)
        draw.text((150, 25), "DETAILED PROJECT REPORT (DPR)", fill="#1A365D")
        draw.text((170, 50), "Scheme: Prime Minister's Employment Generation Programme (PMEGP)", fill="#718096")
        draw.text((40, 90), "Project Title: EcoCraft Food Processing Unit", fill="#2B6CB0")
        draw.text((40, 115), "Business Activity: Manufacturing (Pickle & Fruit Juice Processing)", fill="#2D3748")
        draw.text((40, 140), "Promoter / Applicant: Aarav Rajesh Sharma", fill="#2D3748")
        draw.text((40, 180), "FINANCIAL SUMMARY & MEANS OF FINANCE:", fill="#1A365D")
        draw.text((40, 210), "1. Total Project Cost:             Rs. 15,00,000", fill="#1A202C")
        draw.text((40, 235), "2. Plant & Machinery Cost:         Rs. 10,00,000", fill="#1A202C")
        draw.text((40, 260), "3. Working Capital:                Rs.  5,00,000", fill="#1A202C")
        draw.text((40, 285), "4. Bank Term Loan (80%):           Rs. 12,00,000", fill="#276749")
        draw.text((40, 310), "5. Own Contribution / Margin (20%): Rs.  3,00,000", fill="#276749")
        draw.text((40, 335), "6. Expected Capital Subsidy (35%): Rs.  5,25,000 (Rural Special)", fill="#D69E2E")
        draw.text((40, 380), "Key Sections Verified: Executive Summary, Machinery List, Cash Flow Projections", fill="#718096")
        draw.text((40, 480), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_dpr_text() -> str:
        return (
            "DETAILED PROJECT REPORT (DPR)\n"
            "Project Title: EcoCraft Food Processing Unit\n"
            "Business Type: Manufacturing\n"
            "Promoter: Aarav Rajesh Sharma\n"
            "Total Project Cost: Rs. 15,00,000\n"
            "Bank Loan Required: Rs. 12,00,000\n"
            "Promoter Margin Contribution: Rs. 3,00,000\n"
            "Plant & Machinery: Rs. 10,00,000\n"
            "Working Capital: Rs. 5,00,000\n"
            "Means of Finance Balance Verified\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_udyam_image() -> Image.Image:
        img = Image.new("RGB", (650, 480), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 465)], outline="#1A365D", width=2)
        draw.text((160, 25), "UDYAM REGISTRATION CERTIFICATE", fill="#1A365D")
        draw.text((130, 48), "Ministry of Micro, Small and Medium Enterprises", fill="#718096")
        draw.text((40, 90), "UDYAM REGISTRATION NUMBER:", fill="#718096")
        draw.text((40, 110), "UDYAM-MH-12-0012345", fill="#2B6CB0")
        draw.text((40, 150), "Name of Enterprise: EcoCraft Agro Enterprises", fill="#1A202C")
        draw.text((40, 180), "Name of Entrepreneur: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((40, 210), "Type of Enterprise: Micro", fill="#1A202C")
        draw.text((40, 240), "Major Activity: Manufacturing", fill="#1A202C")
        draw.text((40, 270), "Social Category: Scheduled Caste (SC)", fill="#1A202C")
        draw.text((40, 300), "DIC: Mumbai Suburban, Maharashtra", fill="#1A202C")
        draw.rectangle([(420, 340), (580, 420)], outline="#1A365D", width=1)
        draw.text((435, 360), "[MSME QR CODE]", fill="#718096")
        draw.text((440, 385), "Ministry of MSME", fill="#1A365D")
        draw.text((40, 440), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_udyam_text() -> str:
        return (
            "UDYAM REGISTRATION CERTIFICATE\n"
            "Ministry of Micro, Small and Medium Enterprises\n"
            "UDYAM-MH-12-0012345\n"
            "Name of Enterprise: EcoCraft Agro Enterprises\n"
            "Name of Entrepreneur: Aarav Rajesh Sharma\n"
            "Type of Enterprise: Micro\n"
            "Major Activity: Manufacturing\n"
            "DIC: Mumbai Suburban, Maharashtra\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_10th_image() -> Image.Image:
        img = Image.new("RGB", (650, 450), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 435)], outline="#2B6CB0", width=2)
        draw.text((160, 25), "CENTRAL BOARD OF SECONDARY EDUCATION", fill="#1A365D")
        draw.text((190, 50), "SECONDARY SCHOOL EXAMINATION (CLASS X)", fill="#718096")
        draw.text((220, 75), "MARKS STATEMENT & CERTIFICATE", fill="#2B6CB0")
        draw.text((40, 120), "Roll No: 12145678", fill="#2D3748")
        draw.text((40, 145), "Candidate Name: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((40, 170), "Date of Birth: 15/08/1995", fill="#1A202C")
        draw.text((40, 195), "School: Kendriya Vidyalaya IIT Powai, Mumbai", fill="#1A202C")
        draw.text((40, 230), "ACADEMIC PERFORMANCE SUMMARY:", fill="#1A365D")
        draw.text((40, 260), "1. English: 88/100    2. Mathematics: 92/100    3. Science: 90/100", fill="#2D3748")
        draw.text((40, 285), "4. Social Science: 86/100    5. Hindi: 84/100", fill="#2D3748")
        draw.text((40, 320), "Overall Result: PASS (Cumulative Grade: 88.0%)", fill="#276749")
        draw.text((40, 400), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_10th_text() -> str:
        return (
            "CENTRAL BOARD OF SECONDARY EDUCATION\n"
            "Secondary School Examination (Class X) Marks Statement\n"
            "Roll No: 12145678\n"
            "Name: Aarav Rajesh Sharma\n"
            "DOB: 15/08/1995\n"
            "School: Kendriya Vidyalaya IIT Powai, Mumbai\n"
            "Result: PASS\n"
            "Percentage: 88.0%\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_12th_image() -> Image.Image:
        img = Image.new("RGB", (650, 450), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 435)], outline="#276749", width=2)
        draw.text((150, 25), "MAHARASHTRA STATE BOARD OF SECONDARY & HIGHER SECONDARY", fill="#1A365D")
        draw.text((180, 50), "HIGHER SECONDARY CERTIFICATE (HSC / CLASS XII)", fill="#718096")
        draw.text((210, 75), "CONSOLIDATED MARKSHEET", fill="#276749")
        draw.text((40, 120), "Seat No: M248901", fill="#2D3748")
        draw.text((40, 145), "Candidate Name: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((40, 170), "Stream: Science (PCM)", fill="#1A202C")
        draw.text((40, 195), "College: St. Xavier's Junior College, Mumbai", fill="#1A202C")
        draw.text((40, 230), "SUBJECT SCORES:", fill="#1A365D")
        draw.text((40, 260), "Physics: 89/100    Chemistry: 91/100    Mathematics: 94/100", fill="#2D3748")
        draw.text((40, 285), "English: 85/100    Computer Science: 95/100", fill="#2D3748")
        draw.text((40, 320), "Overall Result: FIRST CLASS WITH DISTINCTION (90.8%)", fill="#276749")
        draw.text((40, 400), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_12th_text() -> str:
        return (
            "MAHARASHTRA STATE BOARD OF SECONDARY & HIGHER SECONDARY EDUCATION\n"
            "Higher Secondary Certificate Examination (Class XII)\n"
            "Seat No: M248901\n"
            "Name: Aarav Rajesh Sharma\n"
            "Stream: Science\n"
            "Result: PASS WITH DISTINCTION\n"
            "Aggregate Score: 90.8%\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_admission_image() -> Image.Image:
        img = Image.new("RGB", (650, 480), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 465)], outline="#744210", width=2)
        draw.text((150, 25), "VEERMATA JIJABAI TECHNOLOGICAL INSTITUTE (VJTI)", fill="#744210")
        draw.text((220, 50), "AUTONOMOUS GOVT. ENGINEERING INSTITUTE", fill="#718096")
        draw.text((210, 75), "PROVISIONAL ADMISSION OFFER LETTER", fill="#2B6CB0")
        draw.text((40, 120), "Admission Ref: VJTI/ADM/2024/BTECH-CS/042", fill="#2D3748")
        draw.text((40, 150), "To: Shri Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((40, 180), "Course: Bachelor of Technology (B.Tech) - Computer Engineering", fill="#1A202C")
        draw.text((40, 210), "Academic Session: 2024-2028 (4-Year Degree Course)", fill="#1A202C")
        draw.text((40, 240), "Category Quota: SC / Central Allotment Round (MHT-CET Merit #1024)", fill="#1A202C")
        draw.text((40, 270), "Admission Status: CONFIRMED UPON FEE REMITTANCE", fill="#276749")
        draw.text((40, 310), "Approved under AICTE & Directorate of Technical Education, Maharashtra.", fill="#718096")
        draw.text((40, 350), "Dean (Academic Admissions), VJTI Mumbai", fill="#1A365D")
        draw.text((40, 440), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_admission_text() -> str:
        return (
            "VEERMATA JIJABAI TECHNOLOGICAL INSTITUTE (VJTI), MUMBAI\n"
            "Provisional Admission Offer Letter\n"
            "Ref No: VJTI/ADM/2024/BTECH-CS/042\n"
            "Student Name: Aarav Rajesh Sharma\n"
            "Course: B.Tech in Computer Engineering (4 Years)\n"
            "Admission Status: Confirmed\n"
            "AICTE / DTE Approved Institution\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_fee_structure_image() -> Image.Image:
        img = Image.new("RGB", (650, 500), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 485)], outline="#2B6CB0", width=2)
        draw.text((150, 25), "VEERMATA JIJABAI TECHNOLOGICAL INSTITUTE (VJTI)", fill="#1A365D")
        draw.text((180, 50), "OFFICIAL INSTITUTIONAL FEE BREAKDOWN & SCHEDULE", fill="#718096")
        draw.text((40, 95), "Program: B.Tech (Computer Engineering) - 4-Year Full-Time", fill="#2D3748")
        draw.text((40, 120), "Student: Aarav Rajesh Sharma", fill="#2D3748")
        draw.text((40, 155), "ANNUAL FEE SCHEDULE (PER ACADEMIC YEAR):", fill="#1A365D")
        draw.text((40, 185), "1. Tuition Fees:                     Rs.   85,000", fill="#1A202C")
        draw.text((40, 210), "2. Development & Lab Charges:        Rs.   20,000", fill="#1A202C")
        draw.text((40, 235), "3. University & Examination Fees:    Rs.    5,000", fill="#1A202C")
        draw.text((40, 260), "4. Library & Tech Resource Fund:     Rs.   10,000", fill="#1A202C")
        draw.text((40, 290), "Total Annual Fee (Per Year):         Rs. 1,20,000", fill="#276749")
        draw.text((40, 320), "Total 4-Year Course Cost:            Rs. 4,80,000", fill="#2B6CB0")
        draw.text((40, 350), "Eligible Education Loan Component:   Rs. 4,50,000", fill="#276749")
        draw.text((40, 390), "Authorized by Finance & Accounts Officer, VJTI Mumbai", fill="#718096")
        draw.text((40, 460), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_fee_structure_text() -> str:
        return (
            "VEERMATA JIJABAI TECHNOLOGICAL INSTITUTE (VJTI)\n"
            "Official Institutional Fee Breakdown & Schedule\n"
            "Candidate: Aarav Rajesh Sharma\n"
            "Course: B.Tech Computer Engineering (4 Years)\n"
            "Annual Tuition Fee: Rs. 85,000\n"
            "Development & Lab Charges: Rs. 20,000\n"
            "University & Exam Fees: Rs. 5,000\n"
            "Library & Tech Fund: Rs. 10,000\n"
            "Total Annual Fees: Rs. 1,20,000\n"
            "Total 4-Year Degree Cost: Rs. 4,80,000\n"
            "SYNTHETIC DEMO SAMPLE"
        )
