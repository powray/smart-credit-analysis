import re
from datetime import datetime

DATE_RE = re.compile(r"(\d{1,2}[\\/\\-.]\d{1,2}[\\/\\-.]\d{2,4})")
AMOUNT_RE = re.compile(r"-?\\£?\\s?\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2})?")

def extract_transactions(ocr_lines):
    transactions = []
    for line in ocr_lines:
        date_m = DATE_RE.search(line)
        amount_m = AMOUNT_RE.search(line)
        if date_m and amount_m:
            date_str = date_m.group(1)
            try:
                # permissive parse (day-first)
                if '/' in date_str:
                    date = datetime.strptime(date_str, "%d/%m/%Y")
                elif '-' in date_str:
                    date = datetime.strptime(date_str, "%d-%m-%Y")
                else:
                    date = None
            except Exception:
                date = None
            try:
                amount = float(amount_m.group(0).replace('£','').replace(',','').replace(' ',''))
            except Exception:
                amount = 0.0
            transactions.append({"date": date_str, "amount": amount, "raw": line})
    return transactions
