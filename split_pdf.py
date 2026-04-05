import sys
from pikepdf import Pdf

sys.setrecursionlimit(2000)

input_pdf_path = r"D:\\resources_psycho\\resources_mega\\mega_carlos_ciencias\\MEGAsync\\libros\\Seguridad_402892130-0XWORD-PENTESTING-CON-KALI-2-0-OCR-pdf.pdf"
output_dir = r"C:\\Users\\carlosmx\\Downloads"

try:
    pdf = Pdf.open(input_pdf_path)
    total_pages = len(pdf.pages)
    print(f"Total pages: {total_pages}")

    num_parts = 5
    pages_per_part = total_pages // num_parts

    for i in range(num_parts):
        start = i * pages_per_part
        end = (i + 1) * pages_per_part if i < num_parts - 1 else total_pages

        part = Pdf.new()
        for page_num in range(start, end):
            part.pages.append(pdf.pages[page_num])

        output_path = f"{output_dir}\\Seguridad_402892130-0XWORD-PENTESTING-CON-KALI-2-0-OCR_part{i+1}.pdf"
        part.save(output_path, linearize=True)
        print(f"Part {i+1}: pages {start+1}-{end} saved")

    pdf.close()
    print("PDF split into 5 parts successfully.")

except Exception as e:
    print(f"Error: {e}")