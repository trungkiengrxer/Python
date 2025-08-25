import re

# Đường dẫn file input
input_file = "D:\Downloads\mb-bank.txt"
# Đường dẫn file output
output_file = "D:\Downloads\config.txt"

# Đọc file và lọc các tên miền
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lưu tên miền dạng REJECT, REJECT-DROP và DIRECT
reject_domains = []
direct_domains = []

for line in lines:
    # Tên miền bị từ chối
    match_reject = re.match(r"DOMAIN-SUFFIX,([\w.-]+),REJECT(-DROP)?", line)
    if match_reject:
        domain = match_reject.group(1)
        reject_domains.append(f"||{domain}^")
        continue

    # Tên miền được phép
    match_direct = re.match(r"DOMAIN-SUFFIX,([\w.-]+),DIRECT", line)
    if match_direct:
        domain = match_direct.group(1)
        direct_domains.append(f"@@||{domain}^")
        continue

# Ghi kết quả ra file mới
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(reject_domains))
    f.write("\n".join(direct_domains))

print(f"Đã ghi {len(reject_domains)} tên miền bị từ chối và {len(direct_domains)} tên miền được phép vào file '{output_file}'.")
