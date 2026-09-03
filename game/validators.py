from game.scoring import calculate_score


def validate_answer(
    level: dict,
    object_id: str,
    selected_process_ids: list[str],
    selected_formula_ids: list[str],
    attempts: int,
    hint_used: bool,
) -> dict:
    target = next(item for item in level["objects"] if item["id"] == object_id)
    expected_processes = set(target["processes"])
    expected_formulas = set(target["formula_ids"])
    selected_processes = set(selected_process_ids)
    selected_formulas = set(selected_formula_ids)

    process_correct = selected_processes == expected_processes
    formula_correct = selected_formulas == expected_formulas

    return {
        "object_id": object_id,
        "object_label": target["label"],
        "selected_process_ids": sorted(selected_processes),
        "selected_formula_ids": sorted(selected_formulas),
        "correct_process_ids": sorted(expected_processes),
        "correct_formula_ids": sorted(expected_formulas),
        "missing_process_ids": sorted(expected_processes - selected_processes),
        "extra_process_ids": sorted(selected_processes - expected_processes),
        "missing_formula_ids": sorted(expected_formulas - selected_formulas),
        "extra_formula_ids": sorted(selected_formulas - expected_formulas),
        "process_correct": process_correct,
        "formula_correct": formula_correct,
        "is_fully_correct": process_correct and formula_correct,
        "attempts": attempts,
        "hint_used": hint_used,
        "explanation": target["explanation"],
        "reasoning_steps": target.get("reasoning_steps", []),
        "score": calculate_score(
            process_correct=process_correct,
            formula_correct=formula_correct,
            attempts=attempts,
            hint_used=hint_used,
        ),
    }
