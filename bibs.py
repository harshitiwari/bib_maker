from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Set up bib dimensions
bib_width, bib_height = 1850, 1000  # in pixels
dpi = 500  # Set to 500 DPI to get accurate scaling

font_bib = ImageFont.truetype("impact.ttf", 500)
font_large = ImageFont.truetype("impact.ttf", 200)
font_medium = ImageFont.truetype("impact.ttf", 100)

# Paths to images
runner_image_path = "runner_image_green.png"
club_logo_path = "club_logo.png"

# Load images and resize as needed
runner_image = Image.open(runner_image_path).resize((450, 450))
club_logo = Image.open(club_logo_path).resize((180, 180))

# Generate individual bib images (1-100)
for bib_number in range(200, 251):
    # Create a blank bib
    bib = Image.new("RGB", (bib_width, bib_height), "white")
    draw = ImageDraw.Draw(bib)

    # Draw thin black outline around the bib
    outline_thickness = 5  # Set thickness in pixels for the outline
    draw.rectangle(
        [(outline_thickness // 2, outline_thickness // 2), 
         (bib_width - outline_thickness // 2, bib_height - outline_thickness // 2)], 
        outline="black", width=outline_thickness
    )

    # Part 1: Header with 5KM RUN FOR FUN
    header_height = int(bib_height * 0.25)
    draw.rectangle([(0, 0), (bib_width, header_height)], fill="green")
    draw.text((bib_width // 2, header_height // 2), "5KM \'RUN FOR FUN\'", font=font_large, fill="white", anchor="mm")

    # Part 2: Middle with runner image (20%) and bib number (80%)
    middle_y = header_height
    middle_height = int(bib_height * 0.6)
    bib.paste(runner_image, (100,320), runner_image)
    draw.text((int(bib_width * 0.6), middle_y + middle_height // 2), str(bib_number), font=font_bib, fill="green", anchor="mm")

    # Part 3: Footer with club logo and name
    footer_y = middle_y + middle_height
    footer_height = bib_height - footer_y
    # Paste the club logo on the left side
    club_logo_x = 20  # Add some padding from the left
    bib.paste(club_logo, (50,800), club_logo)
    # Draw the club name to the right of the logo
    club_name_x = club_logo_x + club_logo.width + 10  # Add padding between logo and text
    draw.text((1000,890), "ADVENTURE SPORTS CLUB, IIT KANPUR", font=font_medium, fill="#05253C", anchor="mm")
    
    # Save each bib as a temporary image file
    bib.save(f"bib_{bib_number}.png")

# Create a PDF with A4 page size
pdf_path = "bibs.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
a4_width, a4_height = A4

# Calculate the dimensions for each bib in points (1 inch = 72 points, 500 DPI = 500/72 points per inch)
bib_width_points = bib_width * 72 / dpi
bib_height_points = bib_height * 72 / dpi

# Set space between bibs
horizontal_margin = 10  # space between columns in points
vertical_margin = 10    # space between rows in points

# Placement parameters for 2 columns and 5 rows on each page
x_offset = 36  # Margin on the left side
y_offset = a4_height - 36 - bib_height_points  # Start at about 1 cm height from the top
bibs_per_row = 2
bibs_per_col = 5
x_spacing = bib_width_points + horizontal_margin
y_spacing = bib_height_points + vertical_margin

# Add bibs to PDF with spacing and outline
for page in range(5):  # Modify as needed for all pages
    for i in range(bibs_per_row):
        for j in range(bibs_per_col):
            bib_num = page * 10 + i * bibs_per_col + j + 1 + 200
            bib_image_path = f"bib_{bib_num}.png"
            x_pos = x_offset + i * x_spacing
            y_pos = y_offset - j * y_spacing
            c.drawImage(bib_image_path, x_pos, y_pos, width=bib_width_points, height=bib_height_points)
    c.showPage()  # Add a new page after filling the current one

c.save()
print(f"PDF saved as {pdf_path}")