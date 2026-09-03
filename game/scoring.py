def calculate_score(
    process_correct: bool,
    formula_correct: bool,
    attempts: int,
    hint_used: bool,
) -> int:
    score = 0
    if process_correct:
        score += 40
    if formula_correct:
        score += 50
    if process_correct and formula_correct and attempts == 1:
        score += 10
    if hint_used:
        score -= 10
    return max(score, 0)

