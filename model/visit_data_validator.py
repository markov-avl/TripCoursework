from datetime import datetime, date
from itertools import chain

from entity import Trip, Visit


class VisitDataValidator:
    def __init__(self, trip: Trip, visits: list[Visit]):
        self._trip = trip
        self._visits = visits

    def validate(self) -> list[str]:
        return sorted([
            *self._check_dates_are_in_period(),
            *self._check_no_date_intresections()
        ])

    def _check_dates_are_in_period(self) -> list[str]:
        return [
            self._error(i, 'дата находится вне периода путешествия')
            for i, visit in enumerate(self._visits)
            if visit.date and (visit.date < self._trip.starts_at or self._trip.ends_at < visit.date)
        ]

    def _check_no_date_intresections(self) -> list[str]:
        return chain.from_iterable(
            (
                self._error(i, f'время посещения пересекается со временем посещения {k + 1}-го места')
                for k in range(i)
                if self._intresects(self._visits[k], visit)
            )
            for i, visit in enumerate(self._visits)
        )

    @staticmethod
    def _error(index: int, text: str) -> str:
        return f'{index + 1}. Место посещения: {text}'

    @staticmethod
    def _intresects(visit_1: Visit, visit_2: Visit) -> bool:
        if visit_1.date and visit_1.time and visit_2.date and visit_2.time:
            start_1 = datetime.combine(visit_1.date, visit_1.time)
            end_1 = start_1 + (datetime.combine(date.min, visit_1.stay_time) - datetime.min)
            start_2 = datetime.combine(visit_2.date, visit_2.time)
            end_2 = start_2 + (datetime.combine(date.min, visit_2.stay_time) - datetime.min)
            return (start_1 <= start_2 <= end_1) or (start_2 <= start_1 <= end_2)
        return False
