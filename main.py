from PyPDF2 import PdfWriter, PdfReader
import csv
import re


def normalize_text(text):
    """Remove special characters and collapse whitespace for matching"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Collapse multiple spaces into single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text


csv_entries = []
text_content = ''
pages_to_keep = []
pages_removed = []
input_pdf = './billing.pdf'
output_pdf = './updatedbilling.pdf'
infile = PdfReader(input_pdf, 'rb')
output = PdfWriter()

# Read CSV file and store returned entries in a list
with open('./billing.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['First'] or row['Last'] or row['Address']:
            csv_entries.append([row['First'], row['Last'], row['Address']])
    

# Read PDF and check each page for matches with CSV entries
with open(input_pdf, 'rb') as pdf_file:
    reader = PdfReader(pdf_file)
    for page_num, page in enumerate(reader.pages):
        text_content = page.extract_text() + "\n"
        text_content_normalized = normalize_text(text_content)
        # Check if page contains all three fields (first name, last name, address) from any entry
        match_found = False
        for entry in csv_entries:
            first, last, address = entry
            # Check if all three fields are present in the page text and if so mark for removal
            first_norm = normalize_text(first)
            last_norm = normalize_text(last)
            address_norm = normalize_text(address)
            if first_norm in text_content_normalized and last_norm in text_content_normalized and address_norm in text_content_normalized:
                match_found = True
                pages_removed.append(page_num)
                break
        # Only keep the page if NO match was found
        if not match_found:
            pages_to_keep.append(page_num)


# Create new PDF with only the pages to keep
for i in pages_to_keep:
    p = infile.pages[i] 
    output.add_page(p)
# Write the output PDF to a file
with open(output_pdf, 'wb') as f:
    output.write(f) 

# Print summary of removed pages
if pages_removed:
    for page in pages_removed:
        print(f'Removed page: {page}')

else:
    print('No pages were removed.')