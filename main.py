from database import create_tables
from models.cpa import CPA
from models.client import Client
from models.tax_filing_assistant import TaxFilingAssistant
from models.tax_return import TaxReturn

# Main program file for managing accounting system
# Handles user input and invokes appropriate methods for CPAs, Clients, Assistants, and Tax Returns

# Display the main menu and navigate to management options
def main_menu():
    while True:
        print("\n=== Accounting System ===")
        print("1. Manage CPAs")
        print("2. Manage Clients")
        print("3. Manage Tax Filing Assistants")
        print("4. Manage Tax Returns")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            manage_cpas()
        elif choice == '2':
            manage_clients()
        elif choice == '3':
            manage_assistants()
        elif choice == '4':
            manage_tax_returns()
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Manage CPA operations
def manage_cpas():
    while True:
        print("\n=== Manage CPAs ===")
        print("1. Add CPA")
        print("2. View CPA")
        print("3. Update CPA Name")
        print("4. Delete CPA")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter CPA Name: ")
            cpa = CPA(name=name)
            cpa.save()
            print(f"CPA added with ID: {cpa.cpa_id}")
        elif choice == '2':
            cpa_id = int(input("Enter CPA ID: "))
            cpa = CPA.get(cpa_id)
            if cpa:
                print(f"CPA ID: {cpa.cpa_id}, Name: {cpa.name}")
            else:
                print("CPA not found.")
        elif choice == '3':
            cpa_id = int(input("Enter CPA ID: "))
            new_name = input("Enter New CPA Name: ")
            cpa = CPA.get(cpa_id)
            if cpa:
                cpa.update_name(new_name)
                print("CPA name updated successfully.")
            else:
                print("CPA not found.")
        elif choice == '4':
            cpa_id = int(input("Enter CPA ID: "))
            cpa = CPA.get(cpa_id)
            if cpa:
                cpa.delete()
                print("CPA deleted successfully.")
            else:
                print("CPA not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Manage Client operations
def manage_clients():
    while True:
        print("\n=== Manage Clients ===")
        print("1. Add Client")
        print("2. View Client")
        print("3. Update Client Information")
        print("4. Delete Client")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter Client Name: ")
            address = input("Enter Client Address: ")
            income = float(input("Enter Client Income: "))
            cpa_id = int(input("Enter CPA ID: "))
            client = Client(name=name, address=address, income=income, cpa_id=cpa_id)
            client.save()
            print(f"Client added with ID: {client.client_id}")
        elif choice == '2':
            client_id = int(input("Enter Client ID: "))
            client = Client.get(client_id)
            if client:
                print(f"Client ID: {client.client_id}, Name: {client.name}, Address: {client.address}, Income: {client.income}, CPA ID: {client.cpa_id}, Materials Submitted: {client.tax_materials_submitted}")
            else:
                print("Client not found.")
        elif choice == '3':
            client_id = int(input("Enter Client ID: "))
            field = input("Enter field to update (name/address/income/cpa_id): ").strip().lower()
            new_value = input("Enter new value: ")
            client = Client.get(client_id)
            if client:
                client.update_field(field, new_value)
                print("Client information updated successfully.")
            else:
                print("Client not found.")
        elif choice == '4':
            client_id = int(input("Enter Client ID: "))
            client = Client.get(client_id)
            if client:
                client.delete()
                print("Client deleted successfully.")
            else:
                print("Client not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Manage Tax Filing Assistant operations
def manage_assistants():
    while True:
        print("\n=== Manage Tax Filing Assistants ===")
        print("1. Add Assistant")
        print("2. View Assistant")
        print("3. Update Assistant Name")
        print("4. Delete Assistant")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter Assistant Name: ")
            assistant = TaxFilingAssistant(name=name)
            assistant.save()
            print(f"Assistant added with ID: {assistant.assistant_id}")
        elif choice == '2':
            assistant_id = int(input("Enter Assistant ID: "))
            assistant = TaxFilingAssistant.get(assistant_id)
            if assistant:
                print(f"Assistant ID: {assistant.assistant_id}, Name: {assistant.name}")
            else:
                print("Assistant not found.")
        elif choice == '3':
            assistant_id = int(input("Enter Assistant ID: "))
            new_name = input("Enter New Assistant Name: ")
            assistant = TaxFilingAssistant.get(assistant_id)
            if assistant:
                assistant.update_name(new_name)
                print("Assistant name updated successfully.")
            else:
                print("Assistant not found.")
        elif choice == '4':
            assistant_id = int(input("Enter Assistant ID: "))
            assistant = TaxFilingAssistant.get(assistant_id)
            if assistant:
                assistant.delete()
                print("Assistant deleted successfully.")
            else:
                print("Assistant not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Manage Tax Return operations
def manage_tax_returns():
    while True:
        print("\n=== Manage Tax Returns ===")
        print("1. Add Tax Return")
        print("2. View Tax Return")
        print("3. Mark Tax Return Filed")
        print("4. Mark Tax Return Checked by CPA")
        print("5. Mark Tax Return Filed by Assistant")
        print("6. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            client_id = int(input("Enter Client ID: "))
            try:
                tax_return = TaxReturn(client_id=client_id)
                tax_return.save()
                print(f"Tax Return added with ID: {tax_return.return_id}")
            except ValueError as e:
                print(e)  # Display the error message
        elif choice == '2':
            client_id = int(input("Enter Client ID: "))
            tax_return = TaxReturn.get(client_id)
            if tax_return:
                print(f"Tax Return ID: {tax_return.return_id}, Client ID: {tax_return.client_id}, Status: {tax_return.status}, Filing Timestamp: {tax_return.filing_timestamp}, Checked by CPA: {tax_return.checked_by_cpa}")
            else:
                print("Tax Return not found.")
        elif choice == '3':
            client_id = int(input("Enter Client ID: "))
            tax_return = TaxReturn.get(client_id)
            if tax_return:
                tax_return.mark_filed()
                print("Tax Return marked as filed.")
            else:
                print("Tax Return not found.")
        elif choice == '4':
            client_id = int(input("Enter Client ID: "))
            tax_return = TaxReturn.get(client_id)
            if tax_return:
                tax_return.mark_checked_by_cpa()
                print("Tax Return marked as checked by CPA.")
            else:
                print("Tax Return not found.")
        elif choice == '5':
            return_id = int(input("Enter Tax Return ID: "))
            tax_return = TaxReturn.get(return_id)
            if tax_return:
                tax_return.mark_filed_by_assistant()
                print("Tax Return marked as filed by assistant.")
            else:
                print("Tax Return not found.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize database and start program
if __name__ == "__main__":
    create_tables()
    main_menu()
