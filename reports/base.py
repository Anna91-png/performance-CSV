from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class BaseReport(ABC):
    """Базовый класс для всех отчётов."""

    @abstractmethod
    def generate(self, data: List[Dict[str, str]]) -> Tuple[List[List], List[str]]:
        """
        Сгенерировать отчёт.
        :param data: список словарей строк CSV
        :return: (rows, headers) — строки таблицы и заголовки
        """
        raise NotImplementedError
