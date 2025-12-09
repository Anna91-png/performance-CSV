from collections import defaultdict
from typing import List, Dict, Tuple
from .base import BaseReport


class PerformanceReport(BaseReport):
    """
    Отчёт по средней эффективности (performance) на позицию.
    Объединяет данные из всех переданных файлов, считает среднее по позициям, сортирует по убыванию.
    """

    def generate(self, data: List[Dict[str, str]]) -> Tuple[List[List], List[str]]:
        perf_by_position = defaultdict(list)

        for row in data:
            position = row.get("position")
            perf_raw = row.get("performance")
            if position is None or perf_raw is None:
                # Пропускаем некорректные строки
                continue
            try:
                performance = float(perf_raw)
            except (TypeError, ValueError):
                # Пропускаем значения, которые нельзя привести к числу
                continue
            perf_by_position[position].append(performance)

        rows = []
        for position, values in perf_by_position.items():
            if not values:
                continue
            avg = sum(values) / len(values)
            rows.append([position, round(avg, 2)])

        # Сортировка по средней эффективности (по убыванию)
        rows.sort(key=lambda r: r[1], reverse=True)
        headers = ["Position", "Average Performance"]
        return rows, headers
