import requests

from lightning.processor import Processor

class AlbyProcessor(Processor):
    BASE_URL = "https://api.getalby.com"

    def __init__(self, api_key: str):
        super().__init__()
        self.token = api_key
        self.active = True
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def create_invoice(
        self,
        amt: int,
        memo: str,
        description: str = "",
        description_hash: str = "",
        currency: str = "btc",
        comment: str = "",
        metadata: dict = {},
        payer_name: str = "",
        payer_email: str = "",
        payer_pubkey: str = "",
    ) -> dict:
        url = f"{self.BASE_URL}/invoices"
        data = {
            "amount": amt,
            "memo": memo,
            "description": description,
            "description_hash": description_hash,
            "currency": currency,
            "comment": comment,
            "metadata": metadata,
            "payer_name": payer_name,
            "payer_email": payer_email,
            "payer_pubkey": payer_pubkey,
        }

        response = self.session.post(url, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(
                f"Error creating invoice: {response.status_code} - {response.text}"
            )

    def has_been_paid(self, payment_hash: str) -> bool:
        url = f"{self.BASE_URL}/invoices/{payment_hash}"

        response = self.session.get(url)
        if response.status_code in [200, 201]:
            invoice = response.json()
            return invoice.get("settled", False)
        elif response.status_code == 404:
            return False
        else:
            raise Exception(
                f"Error checking invoice status: {response.status_code} - {response.text}"
            )

    def get_invoice(self, payment_hash: str) -> dict:
        url = f"{self.BASE_URL}/invoices/{payment_hash}"

        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error retrieving invoice: {response.status_code} - {response.text}"
            )

    def close(self):
        self.session.close()

def main():
    cfg = {"token": "your_api_key_here"}
    alby_processor = AlbyProcessor(cfg["token"])

    try:
        # Create an invoice
        invoice = alby_processor.create_invoice(
            amt=1000, memo="Test Invoice", description="This is a test"
        )
        print(invoice)

        # Check if the invoice has been paid
        payment_hash = invoice["payment_hash"]
        paid = alby_processor.has_been_paid(payment_hash)
        print(f"Has been paid: {paid}")

        # Get invoice details
        invoice_details = alby_processor.get_invoice(payment_hash)
        print(invoice_details)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        alby_processor.close()

if __name__ == "__main__":
    main()