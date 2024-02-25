from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import csv


def draw_receipt(
    canvas, x, y, number, name, phone, amount, good_or_service, tax_rate, date
):
    """
    This function draws a receipt on the PDF.
    It includes the name and the amount of the receipt.
    """
    c = canvas

    print(f"Drawing receipt for {name} with amount {amount} at position ({x}, {y})")

    # draw box around receipt
    c.rect(x, y, A4[1] / 2, A4[0] / 2)

    # Draw title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x, y + 9.8 * cm, "KVITTENS")

    # Draw receipt number
    c.rect(x, y + 9.5 * cm, 4 * cm, -1 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 9 * cm, "Nummer")
    c.setFont("Courier", 16)
    c.drawString(x + 2.7 * cm, y + 8.9 * cm, f"{number}")

    # draw payer block
    c.rect(x + 4.9 * cm, y + A4[0] / 2, 9.95 * cm, -2 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 5 * cm, y + 10 * cm, "Betalare")
    c.setFont("Courier-Bold", 18)
    c.drawString(x + 5.3 * cm, y + 9.3 * cm, f"{name}")
    c.drawString(x + 5.3 * cm, y + 8.6 * cm, f"{phone}")

    # draw good or service block
    c.rect(x, y + 8 * cm, A4[1] / 2, -2.5 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 7.5 * cm, "Specifikation")
    c.setFont("Courier", 16)
    c.drawString(x + 0.1 * cm, y + 6.7 * cm, f"{good_or_service}")

    # moms registration nummer block
    c.rect(x, y + 5.5 * cm, 9 * cm, -0.7 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 5 * cm, "Momsreg.nr/org.nr")
    c.setFont("Courier", 16)
    c.drawString(x + 4 * cm, y + 5 * cm, "<<<<MY ORG NR>>>>")

    # tax block
    c.rect(x, y + 4.8 * cm, A4[1] / 2, -1 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 4 * cm, f"Moms ingår med kr ({tax_rate}%)")
    c.setFont("Courier", 16)
    tax = amount * (tax_rate * 0.01) / (1 + tax_rate * 0.01)
    c.drawString(x + 6 * cm, y + 4 * cm, "{:.2f} kr".format(tax))

    # amount block
    c.rect(x, y + 3.8 * cm, A4[1] / 2, -1 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 3 * cm, "KRONOR")
    c.setFont("Courier-Bold", 20)
    c.drawString(x + 6 * cm, y + 3 * cm, "{:.2f} kr".format(amount))

    # date block
    c.rect(x, y + 2.8 * cm, 6 * cm, -1 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 2 * cm, "Datum")
    c.setFont("Courier", 16)
    c.drawString(x + 2 * cm, y + 2 * cm, f"{date}")

    # city block
    c.rect(x + 6 * cm, y + 2.8 * cm, 6 * cm, -1 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 6.1 * cm, y + 2 * cm, "Ort")
    c.setFont("Courier", 16)
    c.drawString(x + 7.5 * cm, y + 2 * cm, "Stockholm")

    # signature block
    c.rect(x, y, A4[1] / 2, 1.8 * cm)
    c.setFont("Helvetica", 12)
    c.drawString(x + 0.1 * cm, y + 0.5 * cm, "Underskrift")
    c.setFont("Courier", 16)
    c.drawString(x + 5 * cm, y + 0.5 * cm, "____________________")


def create_receipts_pdf(csv_file_path, pdf_file_path, starting_receipt_number=1):
    """
    Creates a PDF file with receipts from a CSV file, containing `name` and `amount` columns.
    Draws 4 receipts per page, in 2 rows and 2 columns.
    """
    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        receipts = list(reader)

    # create the canvas
    c = canvas.Canvas(pdf_file_path, pagesize=landscape(A4))

    # these are the 4 locations where we will draw the receipts
    locations = [(0, A4[0] / 2), (A4[1] / 2, A4[0] / 2), (0, 0), (A4[1] / 2, 0)]

    for index, receipt in enumerate(receipts, 1):
        name = receipt["name"].title()
        date = receipt["date"]
        amount = int(receipt["amount"])
        good_or_service = receipt["good_or_service"]
        tax_rate = int(receipt["tax_rate"])
        # number = starting_receipt_number + index - 1
        number = receipt["row_number"]
        phone = receipt["phone"]

        draw_receipt(
            canvas=c,
            x=locations[index % 4 - 1][0],
            y=locations[index % 4 - 1][1],
            number=number,
            name=name,
            phone=phone,
            amount=amount,
            good_or_service=good_or_service,
            tax_rate=tax_rate,
            date=date,
        )

        # if we have drawn 4 receipts, we need to create a new page
        if index % 4 == 0 and index != 0:
            c.showPage()

    c.save()


if __name__ == "__main__":
    '''
    example:
    row_number,date,phone,amount,name,good_or_service,tax_rate
    42,2024-01-31,+46123456789,200,John Doe,Konstundervisning barn och undgomar,6
    '''
    csv_file_path = "input.csv"
    pdf_file_path = "output.pdf"
    create_receipts_pdf(csv_file_path, pdf_file_path, starting_receipt_number=1)
