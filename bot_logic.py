from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must consist of exactly 10 digits.")
        super().__init__(value)
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def show_phones(self):
        return ', '.join(str(p) for p in self.phones)

    def remove_phone(self, phone):
        phone_to_remove = next((p for p in self.phones if p.value == phone), None)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"No phone found with number '{phone}'.")

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)
    
    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("Birthday is already set.")
        self.birthday = Birthday(birthday)
    
    def show_birthday(self):
        return self.birthday.value if self.birthday else "Birthday is not set."

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No record found with name '{name}'.")
        
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date:
                    if birthday_this_year.weekday() in (5, 6):  # 5 - субота, 6 - неділя
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays



# Тестування реалізації
# if __name__ == "__main__":
#     # Створення нової адресної книги
#     book = AddressBook()

#     # Створення запису для John
#     john_record = Record("John")
#     john_record.add_phone("1234567890")
#     john_record.add_phone("5555555555")

#     # Додавання запису John до адресної книги
#     book.add_record(john_record)

#     # Створення та додавання нового запису для Jane
#     jane_record = Record("Jane")
#     jane_record.add_phone("9876543210")
#     book.add_record(jane_record)

#     # Виведення всіх записів у книзі
#     for name, record in book.data.items():
#         print(record)

#     # Знаходження та редагування телефону для John
#     john = book.find("John")
#     john.edit_phone("1234567890", "1112223333")

#     print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#     # Пошук конкретного телефону у записі John
#     found_phone = john.find_phone("5555555555")
#     print(f"{john.name.value}: {found_phone}")  # Виведення: 5555555555

#     # Видалення запису Jane
#     book.delete("Jane")
#     print(f"Address book after deletion: {list(book.data.keys())}")
