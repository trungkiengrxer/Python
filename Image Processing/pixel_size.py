from PIL import Image

# Mở hình ảnh
img = Image.open("D:/Downloads/Lenna_(test_image).png")

# Lấy kích thước hình ảnh
width, height = img.size
print(f"Kích thước hình ảnh: {width} x {height}")

# Lấy thông tin DPI
dpi = img.info.get('dpi', (72, 72))  # Mặc định là 72 DPI nếu không có thông tin

# Kích thước pixel trong inch
pixel_size_inch = (1 / dpi[0], 1 / dpi[1])
print(f"Kích thước của 1 pixel: {pixel_size_inch[0]} inch x {pixel_size_inch[1]} inch")
