from bot_logic import AddressBook, Record
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
                return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Not enough arguments provided."
    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record_phone = record.find_phone(phone)
    if record_phone:
        raise ValueError(f"{phone} is already in use")
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.find_phone(old_phone):
        raise ValueError(f"{old_phone} number is not in {name}'s address book.")
    record.edit_phone(old_phone, new_phone)
    return f"Phone number for {name} has been changed. {record}"


@input_error
def show_phone(args, book: AddressBook):
    name = args[0] 
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}'s phones are {record.show_phones()}"

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return f"Birthday for {name} has been added. {record}"

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}'s birthday is {record.show_birthday()}"

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    return "\n".join([f"{item['name']} - {item['congratulation_date']}" for item in upcoming])
