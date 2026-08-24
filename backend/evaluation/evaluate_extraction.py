import json
from pathlib import Path

from app.models.request import RFQRequest
from app.services.extractor import RFQExtractor


GOLDEN_SET_PATH = Path("evaluation/golden_set.json")

# 값이 명확하게 정규화되는 필드들만 자동 exact-match 평가
EVALUATED_FIELDS = [
    "country",
    "countries",
    "sample_size",
    "gender",
    "translation_required",
    "programming_required",
    "overlay_required",
    "project_scope",
    "loi",
    "ir",
    "languages",
    "rush",
    "currency",
]


def load_golden_set():
    with open(
        GOLDEN_SET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def normalize(value):
    if isinstance(value, str):
        return value.strip().lower()

    if isinstance(value, list):
        return sorted(
            normalize(item)
            for item in value
        )

    return value


def main():
    golden_set = load_golden_set()
    extractor = RFQExtractor()

    total_fields = 0
    correct_fields = 0
    failed_cases = []

    print("\nRFQ Extraction Evaluation")
    print("=" * 50)

    for case in golden_set:
        email = case["email"]
        expected = case["expected"]

        request = RFQRequest(
            from_name=email["from_name"],
            from_email=email["from_email"],
            subject=email["subject"],
            email_body=email["email_body"],
        )

        try:
            extraction_result = extractor.extract(request)
            actual_model = extraction_result["extraction"]
            actual = actual_model.model_dump()

        except Exception as error:
            print(f"\n❌ {case['id']} - Extraction failed")
            print(f"   {error}")

            failed_cases.append({
                "id": case["id"],
                "error": str(error),
            })

            continue

        case_correct = 0
        case_total = 0

        print(f"\n{case['id']} - {case['description']}")

        for field in EVALUATED_FIELDS:
            expected_value = expected.get(field)
            actual_value = actual.get(field)

            is_correct = (
                normalize(expected_value)
                == normalize(actual_value)
            )

            total_fields += 1
            case_total += 1

            if is_correct:
                correct_fields += 1
                case_correct += 1
            else:
                print(f"   ❌ {field}")
                print(f"      Expected: {expected_value}")
                print(f"      Actual:   {actual_value}")

        case_accuracy = (
            case_correct / case_total * 100
            if case_total
            else 0
        )

        print(
            f"   Accuracy: "
            f"{case_correct}/{case_total} "
            f"({case_accuracy:.1f}%)"
        )

    overall_accuracy = (
        correct_fields / total_fields * 100
        if total_fields
        else 0
    )

    print("\n" + "=" * 50)
    print("Evaluation Summary")
    print("=" * 50)

    print(f"Test Cases:       {len(golden_set)}")
    print(f"Fields Evaluated: {total_fields}")
    print(f"Correct Fields:   {correct_fields}")
    print(f"Field Accuracy:   {overall_accuracy:.2f}%")
    print(f"Failed Calls:     {len(failed_cases)}")


if __name__ == "__main__":
    main()