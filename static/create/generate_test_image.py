from PIL import Image, ImageDraw

# Create a new image with white background
width = 800
height = 600
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Draw a simple house outline
# House body
draw.polygon([(300, 400), (500, 400), (500, 250), (300, 250)], outline='black', fill='white', width=3)
# Roof
draw.polygon([(250, 250), (550, 250), (400, 150)], outline='black', fill='white', width=3)
# Door
draw.rectangle([(375, 300), (425, 400)], outline='black', fill='white', width=3)
# Window left
draw.rectangle([(325, 300), (360, 335)], outline='black', fill='white', width=3)
# Window right
draw.rectangle([(440, 300), (475, 335)], outline='black', fill='white', width=3)
# Sun
draw.arc([50, 50, 150, 150], 0, 360, fill='black', width=3)
# Sun rays
for i in range(0, 360, 45):
    start_x = 100 + 60 * (i/360)
    start_y = 100 + 60 * (i/360)
    end_x = 100 + 80 * (i/360)
    end_y = 100 + 80 * (i/360)
    draw.line([(start_x, start_y), (end_x, end_y)], fill='black', width=3)

# Save the image
image.save('../images/test-page.png', 'PNG')
print("Test image created at static/images/test-page.png")
