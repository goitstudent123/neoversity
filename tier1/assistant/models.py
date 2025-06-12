from collections import UserDict
from datetime import date, datetime, timedelta
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Field(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field[str]):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field[str]):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        super().__init__(value)


class Birthday(Field[date]):
    def __init__(self, value: str):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str, phone: Optional[str] = None, birthday: Optional[str] = None):
        self.name = Name(name)
        self.phones: list[Phone] = [] if phone is None else [Phone(phone)]
        self.birthday: Optional[Birthday] = None if birthday is None else Birthday(birthday)

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> bool:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        bday_str = (
            f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        )
        return f"Contact name: {self.name.value}, phones: {phones_str}{bday_str}"


class AddressBook(UserDict):
    def __init__(self, initial_data: Optional[dict[str, Record]] = None):
        super().__init__()
        if initial_data:
            self.data.update(initial_data)

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(
        self, today: Optional[date] = None, date_format: str = "%d.%m.%Y"
    ) -> list[dict]:
        def adjust_weekend(current_date: date) -> date:
            if current_date.weekday() == 5:
                return current_date + timedelta(days=2)
            elif current_date.weekday() == 6:
                return current_date + timedelta(days=1)
            return current_date

        today = today or datetime.today().date()
        end_date = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value
            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                birthday_this_year = date(today.year, 3, 1)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= end_date:
                congratulation_date = adjust_weekend(birthday_this_year)
                result.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime(date_format),
                    }
                )

        return result
