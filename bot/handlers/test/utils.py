from typing import Dict, Optional
from .constants import SCORE_CATEGORIES
from infrastructure.database.models import Test


def generate_test_results(answers: Dict[int, int]) -> str:
    question_categories = [
        "Тревожность",
        "Тревожность",
        "Тревожность",
        "Выгорание",
        "Выгорание",
        "Обида",
        "Обида",
        "Самокритика/Вина",
        "Самокритика/Вина",
        "Стыд",
        "Стыд",
        "Стыд",
        "Страх перемен",
        "Разобщённость с собой",
    ]

    category_scores: Dict[str, int] = {category: 0 for category in SCORE_CATEGORIES}

    for question_num, score in answers.items():
        if 1 <= question_num <= len(question_categories):
            category = question_categories[question_num - 1]
            category_scores[category] += score

    interpretation: str = str()
    for category in category_scores:
        score = category_scores[category]
        for score_range in SCORE_CATEGORIES[category]:
            if score_range[0] <= score <= score_range[1]:
                interpretation += f"\n<b>{category}</b> ({score}): <u>{score_range[2]}</u>"
                break

    return interpretation


def get_test_interpretation(test: Test) -> Optional[Dict[int, int]]:
    answers = {}
    for i in range(1, 15):
        score = getattr(test, f'score_test_{i}')
        if score is None:
            return None
        answers[i] = score
    return answers