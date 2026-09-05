import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FIXTURES_DIR = Path(__file__).resolve().parent / "test_fixtures"
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

def create_wage_register_blurred():
    """Generates a blurred, photographed wage register sample (JPG)."""
    img = Image.new("RGB", (1200, 1600), color=(245, 240, 230)) # Aged paper color
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([60, 60, 1140, 160], fill=(220, 210, 195), outline=(100, 90, 80), width=2)
    draw.text((100, 80), "FORM X - REGISTER OF WAGES [Rule 26(1)]", fill=(40, 30, 20))
    draw.text((100, 115), "ESTABLISHMENT: SHRAMIK TEXTILES PVT LTD - WAGE PERIOD: JAN 2026", fill=(60, 50, 40))

    # Grid / Table Headers
    draw.rectangle([60, 180, 1140, 1450], outline=(120, 110, 100), width=2)
    
    # Table rows
    rows = [
        ("Emp ID", "Worker Name", "Skill Cat", "Normal Rate", "OT Hrs", "OT Pay", "Gross Wages", "Deductions"),
        ("E-101", "Ramesh Kumar", "Skilled", "Rs. 740/day", "14.5 hrs", "Rs. 2,400", "Rs. 20,900", "Rs. 1,800"),
        ("E-102", "Sita Devi", "Unskilled", "Rs. 510/day", "8.0 hrs", "Rs. 1,100", "Rs. 14,360", "Rs. 1,200"),
        ("E-103", "Anil Sharma", "Semi-Skilled", "Rs. 620/day", "0.0 hrs", "Rs. 0", "Rs. 16,120", "Rs. 1,400"),
    ]

    y = 200
    for i, row in enumerate(rows):
        line_y = y + 50
        draw.line([60, line_y, 1140, line_y], fill=(160, 150, 140), width=1 if i > 0 else 2)
        # Draw columns
        x_positions = [80, 200, 400, 540, 680, 800, 930, 1050]
        for text, x in zip(row, x_positions):
            draw.text((x, y + 15), text, fill=(20, 20, 20) if i==0 else (50, 40, 30))
        y += 60

    # Add simulated stamp and handwriting blur
    draw.ellipse([800, 1100, 1050, 1350], outline=(180, 40, 40), width=4)
    draw.text((840, 1210), "PAID & VERIFIED\n31-JAN-2026", fill=(180, 40, 40))

    # Apply Gaussian Blur filter to simulate blurry photo
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=2.5))
    save_path = FIXTURES_DIR / "wage_register_blurred.jpg"
    blurred_img.save(save_path, "JPEG", quality=75)
    print(f"Created fixture: {save_path}")

def create_safety_inspection_clean():
    """Generates a clean safety inspection PDF document."""
    img = Image.new("RGB", (1200, 1600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header Banner
    draw.rectangle([0, 0, 1200, 140], fill=(24, 43, 73)) # Ministry Dark Navy
    draw.text((80, 40), "GOVERNMENT OF INDIA - MINISTRY OF LABOUR & EMPLOYMENT", fill=(255, 255, 255))
    draw.text((80, 75), "ANNUAL FACTORY SAFETY & HEALTH COMPLIANCE REPORT", fill=(200, 225, 255))

    # Document Body
    draw.text((80, 180), "Establishment Name: Apex Industrial Solutions Ltd", fill=(30, 30, 30))
    draw.text((80, 215), "State: Maharashtra | Sector: Chemical Manufacturing | Headcount: 45", fill=(60, 60, 60))
    draw.line([80, 250, 1120, 250], fill=(200, 200, 200), width=2)

    sections = [
        ("I. Safety Committee Record", "Safety Committee Meeting Record: Meeting held quarterly on 15-Dec-2025. Minutes logged in Form 12. Safety Officer Appointed."),
        ("II. Health Examination Record", "Health Examination Record: Annual medical examination conducted for 45 hazardous section workers. Form 7 certificates issued."),
        ("III. Accident Record & Log", "Accident Record: 0 Fatalities, 1 Minor First-Aid Incident Logged in Form 24 accident register."),
        ("IV. Hazardous Process Operations", "Hazardous Process Flag: TRUE. Solvent storage unit classified under Schedule III hazardous process controls."),
    ]

    y = 280
    for title, desc in sections:
        draw.rectangle([80, y, 1120, y + 40], fill=(240, 244, 250))
        draw.text((95, y + 10), title, fill=(24, 43, 73))
        y += 50
        draw.text((95, y), desc, fill=(50, 50, 50))
        y += 80

    save_path = FIXTURES_DIR / "safety_inspection_clean.pdf"
    # Save directly as PDF from PIL
    img.save(save_path, "PDF", resolution=150.0)
    print(f"Created fixture: {save_path}")

def create_factory_license_scanned():
    """Generates a scanned factory registration & contract labour license (PDF)."""
    img = Image.new("RGB", (1200, 1600), color=(250, 250, 248))
    draw = ImageDraw.Draw(img)

    draw.rectangle([100, 80, 1100, 220], outline=(0, 51, 102), width=3)
    draw.text((150, 110), "DEPARTMENT OF FACTORIES INSPECTORATE", fill=(0, 51, 102))
    draw.text((150, 150), "LICENSE TO WORK A FACTORY (FORM 4)", fill=(0, 51, 102))

    fields = [
        "Registration Number: LIC/MUM/2025/FL-4402",
        "Factory Name: Supreme Auto Components India Pvt Ltd",
        "Declared Headcount: 250 Workers",
        "Contractor License Record: License CL/2024/9918 Granted for 120 Contract Labourers",
        "Contract Labour Count: 120",
        "ISMW Count: 25 Inter-State Migrant Workers",
        "ISMW Compliance Record: Passbooks issued, Displacement Allowance paid in full as per Section 14",
        "Commencement Notice Record: Notice of commencement filed under Form I on 10-Jan-2024",
    ]

    y = 260
    for f_text in fields:
        draw.rectangle([100, y, 1100, y + 55], outline=(210, 210, 210), width=1)
        draw.text((120, y + 18), f_text, fill=(30, 30, 30))
        y += 75

    # Simulated official stamp
    draw.ellipse([750, 1050, 1000, 1300], outline=(0, 70, 160), width=3)
    draw.text((780, 1160), "CHIEF INSPECTOR\nOF FACTORIES", fill=(0, 70, 160))

    # Add slight scan noise/rotation simulation
    scanned_img = img.rotate(0.5, expand=False, fillcolor=(250,250,248))
    save_path = FIXTURES_DIR / "factory_license_scanned.pdf"
    scanned_img.save(save_path, "PDF", resolution=150.0)
    print(f"Created fixture: {save_path}")

if __name__ == "__main__":
    create_wage_register_blurred()
    create_safety_inspection_clean()
    create_factory_license_scanned()
