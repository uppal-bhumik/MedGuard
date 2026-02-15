from PIL import Image, ImageDraw, ImageFont
import os

def create_prescription():
    # Create white canvas (Letter size-ish)
    width = 800
    height = 1000
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Try to load a font, fallback to default
    try:
        # Arial is common on Windows
        title_font = ImageFont.truetype("arial.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw Header
    d.text((50, 50), "CITY GENERAL CLINIC", font=title_font, fill=(0, 0, 139))
    d.text((50, 100), "Dr. John Smith, MD", font=text_font, fill='black')
    d.text((50, 130), "Cardiology & General Medicine", font=small_font, fill='gray')
    d.text((600, 50), "Date: 15 Oct 2025", font=text_font, fill='black')
    
    # Draw Separator
    d.line((50, 160, 750, 160), fill='black', width=2)

    # Patient Info
    d.text((50, 180), "Patient Name: Demo User", font=text_font, fill='black')
    d.text((50, 210), "Age: 45   Sex: M", font=text_font, fill='black')

    # Rx Symbol
    d.text((50, 270), "Rx", font=title_font, fill='black')

    # Medicines List
    medicines = [
        "1. Amoxicillin 500mg",
        "   - Take 1 tablet every 8 hours (Three times a day)",
        "   - Complete full course (5 days)",
        "",
        "2. Paracetamol 650mg",
        "   - Take 1 tablet for fever/pain",
        "   - Max 3 tablets per day",
        "",
        "3. Cetirizine 10mg",
        "   - Take 1 tablet at night",
        "   - Once Daily"
    ]

    y = 330
    for line in medicines:
        d.text((70, y), line, font=text_font, fill='black')
        y += 35

    # Footer / Signature
    d.line((50, 850, 750, 850), fill='black', width=2)
    d.text((500, 900), "Dr. John Smith", font=text_font, fill='black')
    d.text((500, 880), "(Signature)", font=small_font, fill='gray')
    
    # Save to Desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(desktop, "sample_prescription.jpg")
    img.save(output_path)
    print(f"Prescription saved to: {output_path}")

if __name__ == "__main__":
    create_prescription()
