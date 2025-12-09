import pytest
from reports.performance import PerformanceReport


def test_performance_report_basic():
    data = [
        {"position": "Backend Developer", "performance": "4.8"},
        {"position": "Backend Developer", "performance": "4.6"},
        {"position": "QA Engineer", "performance": "4.5"},
    ]
    report = PerformanceReport()
    rows, headers = report.generate(data)

    assert headers == ["Position", "Average Performance"]
    # Проверяем сортировку по убыванию
    assert rows[0][0] == "Backend Developer"
    assert rows[0][1] == 4.7
    assert rows[1][0] == "QA Engineer"
    assert rows[1][1] == 4.5


def test_performance_report_skips_invalid_rows():
    data = [
        {"position": "Data Scientist", "performance": "4.6"},
        {"position": "Data Scientist", "performance": "not-a-number"},
        {"position": None, "performance": "4.0"},
        {"position": "Data Scientist", "performance": ""},
    ]
    report = PerformanceReport()
    rows, _ = report.generate(data)

    # Должно посчитать только валидные значения
    assert rows == [["Data Scientist", 4.6]]


def test_performance_report_multiple_positions():
    data = [
        {"position": "DevOps Engineer", "performance": "4.9"},
        {"position": "Frontend Developer", "performance": "4.7"},
        {"position": "Frontend Developer", "performance": "4.7"},
        {"position": "DevOps Engineer", "performance": "4.9"},
    ]
    report = PerformanceReport()
    rows, _ = report.generate(data)

    assert rows[0] == ["DevOps Engineer", 4.9]
    assert rows[1] == ["Frontend Developer", 4.7]
