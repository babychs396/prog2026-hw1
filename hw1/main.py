import os

def load_contact_book(path: str) -> list[tuple[str, str, str]]:
    if not os.path.exists(path):
        return []

    with open(path, mode="r") as file:
        result = []
        for line in file.readlines():
            first_name, last_name, email = line.strip().split()
            result.append((first_name, last_name, email))
        return result


def print_contact_book(contact_book: list[tuple[str, str, str]]):
    for i, contact in enumerate(contact_book):
        print(f"[{i}] {contact}")


def save_contact_book(path: str, contact_book: list[tuple[str, str, str]]) -> None:
    with open(path, mode="w") as file:
        for contact in contact_book:
            file.write(" ".join(contact) + "\n")


def add_contact(
    contact_book: list[tuple[str, str, str]], new_contact: tuple[str, str, str]
) -> None:
    for contact in contact_book:
        if contact[2] == new_contact[2]:
            print(f"Contact with email {new_contact[2]} already in contact book.")
            return

    contact_book.append(new_contact)


def get_new_contact() -> tuple[str, str, str]:
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")

    return first_name, last_name, email


def remove_contact(contact_book: list[tuple[str, str, str]]):
    index = None

    while not index:
        new_index = int(input("Enter index of contact to remove: "))
        if new_index < 0 or new_index >= len(contact_book):
            print("Invalid index. Try again.")
        else:
            index = new_index

    contact_book.pop(index)


HELP_TEXT = """
Allowed commands:
- add
- remove
- print
- exit
- help
""".strip()

def main():
    contact_book = load_contact_book("./contacts.txt")
    print_contact_book(contact_book)

    is_running = True
    while is_running:
        command = input("Enter command: ").strip().lower()

        if command == "help":
            print(HELP_TEXT)
        elif command == "add":
            add_contact(contact_book, get_new_contact())
        elif command == "remove":
            print_contact_book(contact_book)
            remove_contact(contact_book)
        elif command == "print":
            print_contact_book(contact_book)
        elif command == "exit":
            is_running = False
        else:
            print(f"Unknown command {command}. Use \"help\" to get a list of allowd commands.")

    save_contact_book("./contacts.txt", contact_book)

main()
