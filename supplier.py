
class Supplier:
    def __init__(self, supplier_id: str, name: str,
                 contact_email: str) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Contact Email: {self.contact_email}")
