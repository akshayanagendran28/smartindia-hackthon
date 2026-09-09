# -*- coding: utf-8 -*-
"""
Synthetic Test Document Generator
Creates 100% synthetic, fictitious demo documents (Images and text manifests)
for all 6 document types for Smart India Hackathon jury testing:
- docAadhaar (Fake Aadhaar Card)
- docPan (Fake PAN Card)
- docCaste (Fake SC Caste Certificate)
- docIncome (Fake Income Certificate)
- docDpr (Fake DPR Project Report)
- docUdyam (Fake Udyam Certificate)

Important: ZERO personally identifiable information is used or created.
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
            ("docUdyam", "sample_synthetic_udyam.png", cls._create_udyam_image, cls._get_udyam_text)
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
        # Saffron & Green header lines
        draw.rectangle([(0, 0), (650, 8)], fill="#FF9933")
        draw.rectangle([(0, 392), (650, 400)], fill="#138808")
        draw.rectangle([(10, 10), (640, 390)], outline="#2B6CB0", width=2)
        
        # Emblems & Text
        draw.text((180, 25), "भारत सरकार / Government of India", fill="#1A365D")
        draw.text((130, 45), "भारतीय विशिष्ट पहचान प्राधिकरण (UIDAI)", fill="#2D3748")
        
        # Photo box
        draw.rectangle([(40, 90), (160, 240)], outline="#4A5568", width=2, fill="#EDF2F7")
        draw.text((60, 150), "[PHOTO]", fill="#718096")
        
        # Details
        draw.text((190, 100), "नाम / Name: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((190, 135), "जन्म तिथि / DOB: 15/08/1995", fill="#1A202C")
        draw.text((190, 170), "लिंग / Gender: पुरुष / Male", fill="#1A202C")
        
        # Aadhaar Number (Verhoeff valid synthetic: 2345 6789 1238)
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
        draw.text((150, 28), "INCOME TAX DEPARTMENT - GOVT. OF INDIA", fill="#FFFFFF")
        
        # Photo & Sign
        draw.rectangle([(40, 90), (160, 230)], outline="#4A5568", width=1, fill="#FFFFFF")
        draw.text((65, 150), "[PHOTO]", fill="#718096")
        draw.rectangle([(40, 250), (160, 290)], outline="#CBD5E0", fill="#FFFFFF")
        draw.text((55, 260), "[SIGNATURE]", fill="#718096")

        # PAN Details
        draw.text((190, 80), "स्थायी लेखा संख्या / PAN", fill="#718096")
        draw.text((190, 105), "ABCPS1234F", fill="#2B6CB0")
        draw.text((190, 145), "Name: Aarav Rajesh Sharma", fill="#1A202C")
        draw.text((190, 185), "Father's Name: Rajesh Sharma", fill="#1A202C")
        draw.text((190, 225), "Date of Birth: 15/08/1995", fill="#1A202C")
        draw.text((450, 350), "[SYNTHETIC SAMPLE]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_pan_text() -> str:
        return (
            "INCOME TAX DEPARTMENT\n"
            "GOVT OF INDIA\n"
            "Permanent Account Number Card\n"
            "ABCPS1234F\n"
            "Name: Aarav Rajesh Sharma\n"
            "Father's Name: Rajesh Sharma\n"
            "DOB: 15/08/1995\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_caste_image() -> Image.Image:
        img = Image.new("RGB", (650, 500), color=(255, 255, 250))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 485)], outline="#744210", width=2)
        draw.text((200, 30), "GOVERNMENT OF MAHARASHTRA", fill="#744210")
        draw.text((150, 55), "Office of the Sub-Divisional Magistrate, Mumbai", fill="#2D3748")
        draw.text((220, 85), "CASTE CERTIFICATE", fill="#1A365D")
        draw.line([(210, 105), (380, 105)], fill="#1A365D", width=2)

        draw.text((40, 130), "Certificate No: CC/MH/2024/09876", fill="#2D3748")
        draw.text((450, 130), "Date: 12/04/2023", fill="#2D3748")

        body = (
            "This is to certify that Shri Aarav Rajesh Sharma,\n"
            "Son of Shri Rajesh Sharma, residing at Mumbai,\n"
            "belongs to the Mahar Caste, which is recognized as a\n"
            "Scheduled Caste (SC) under the Constitution (Scheduled Castes)\n"
            "Order, 1950 as amended from time to time."
        )
        draw.text((40, 180), body, fill="#1A202C")
        
        # Stamp & Seal
        draw.rectangle([(420, 360), (580, 440)], outline="#C53030", width=2)
        draw.text((435, 375), "[OFFICIAL SEAL]", fill="#C53030")
        draw.text((430, 400), "Sub-Divisional Magistrate", fill="#2D3748")
        draw.text((40, 460), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
        return img

    @staticmethod
    def _get_caste_text() -> str:
        return (
            "Government of Maharashtra\n"
            "Office of the Sub-Divisional Magistrate, Mumbai Suburban\n"
            "Certificate No: CC/MH/2024/09876\n"
            "This is to certify that Shri Aarav Rajesh Sharma belongs to Mahar community, "
            "which is recognized as a Scheduled Caste (SC) under the Constitution order.\n"
            "Issuing Authority: Sub-Divisional Magistrate\n"
            "Date: 12/04/2023\n"
            "SYNTHETIC DEMO SAMPLE"
        )

    @staticmethod
    def _create_income_image() -> Image.Image:
        img = Image.new("RGB", (650, 500), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(15, 15), (635, 485)], outline="#276749", width=2)
        draw.text((200, 30), "GOVERNMENT OF MAHARASHTRA", fill="#22543D")
        draw.text((180, 55), "Revenue Department - Tahsildar Office", fill="#2D3748")
        draw.text((210, 85), "INCOME CERTIFICATE", fill="#1A365D")
        draw.line([(200, 105), (390, 105)], fill="#1A365D", width=2)

        draw.text((40, 130), "Certificate No: INC/MH/2024/54321", fill="#2D3748")
        draw.text((450, 130), "Date: 15/05/2024", fill="#2D3748")

        body = (
            "This is to certify that on inquiry, the Annual Family Income\n"
            "of Shri Aarav Rajesh Sharma, residing at Mumbai Suburban,\n"
            "from all sources is assessed as Rs. 1,80,000\n"
            "(Rupees One Lakh Eighty Thousand Only) per annum.\n\n"
            "This certificate is valid for Financial Years 2024-2027."
        )
        draw.text((40, 180), body, fill="#1A202C")
        
        draw.rectangle([(420, 360), (580, 440)], outline="#276749", width=2)
        draw.text((440, 375), "[OFFICIAL SEAL]", fill="#276749")
        draw.text((450, 400), "Tahsildar, Mumbai", fill="#2D3748")
        draw.text((40, 460), "[SYNTHETIC TEST DOCUMENT - SIH 2026]", fill="#E53E3E")
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
