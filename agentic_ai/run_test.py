"""
Test script to run the Timetable Analyzer system with mock data.
"""
import sys
import json
import logging
from datetime import datetime, date

# Fix Vietnamese character output on Windows console
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from agentic_ai.main import generate_learning_path
from agentic_ai.test_data.mock_student import create_mock_student_data


def json_serializer(obj):
    """Custom JSON serializer for dates and enums"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, 'value'):  # Enum
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def run_test(student_name: str, student_data: dict):
    """Run test for a specific student"""
    print(f"\n{'='*60}")
    print(f"Testing: {student_name}")
    print(f"{'='*60}")

    result = generate_learning_path(
        student_profile=student_data["student_profile"],
        academic_data=student_data["academic_data"],
        psychology_data=student_data["psychology_data"],
        timetable=student_data.get("timetable"),
        report_card=student_data.get("report_card"),
        study_habits=student_data.get("study_habits"),
    )

    # Print summary
    print(f"\nStudent ID: {result.get('student_id', 'N/A')}")
    print(f"Student Name: {result.get('student_name', 'N/A')}")
    print(f"Processing Time: {result.get('processing_time_seconds', 0):.2f}s")

    # Print weak subjects analysis
    weak_subjects = result.get("weak_subjects_analysis", [])
    if weak_subjects:
        print(f"\nWeak Subjects ({len(weak_subjects)}):")
        for ws in weak_subjects:
            topics_str = ", ".join(ws.get("weak_topics", [])[:3])
            source = ws.get("source", "")
            classification = ws.get("classification", "")
            print(f"  - {ws['subject']}: {ws['average_score']:.1f}/10 "
                  f"(gap: {ws['gap']:.1f}) [{source}]"
                  + (f" - {classification}" if classification else ""))
            if topics_str:
                print(f"    Topics: {topics_str}")
    else:
        print("\nNo weak subjects found!")

    # Print weekly study schedule
    schedule = result.get("weekly_study_schedule")
    if schedule:
        entries = schedule.get("entries", [])
        print(f"\nWeekly Study Schedule ({len(entries)} sessions, "
              f"{schedule.get('total_supplementary_hours', 0)}h/week):")
        print(f"  Subjects covered: {', '.join(schedule.get('weak_subjects_covered', []))}")
        print()
        for entry in entries:
            print(f"  {entry['day']:10s} {entry['start']}-{entry['end']}  "
                  f"{entry['subject']:8s}  {entry['activity']}")
            if entry.get("topics"):
                print(f"{'':12s} → {', '.join(entry['topics'][:2])}")

        if schedule.get("notes"):
            print(f"\n  Notes:")
            for note in schedule["notes"]:
                print(f"    • {note}")
    else:
        print("\nNo weekly schedule generated (missing study habits data?)")

    # Print AI summary status
    ai_summary = result.get("ai_summary")
    if ai_summary:
        print(f"\nAI Summary:\n  {ai_summary}")
    else:
        print("\nAI Summary: None (feature reserved for future use)")

    return result


def main():
    print("="*60)
    print("TIMETABLE ANALYZER SYSTEM TEST")
    print("Supplementary Study Schedule Generator")
    print("="*60)

    # Test with default student profile
    test_cases = [
        ("Default Student (Trịnh Vỹ Kiệt - 12A2)", create_mock_student_data),
    ]

    results = []
    for name, data_creator in test_cases:
        try:
            student_data = data_creator()
            result = run_test(name, student_data)
            has_schedule = result.get("weekly_study_schedule") is not None
            results.append({"name": name, "success": has_schedule})
        except Exception as e:
            print(f"\nERROR testing {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({"name": name, "success": False, "error": str(e)})

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    successful = sum(1 for r in results if r["success"])
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    # Save full result to file for inspection
    print("\nSaving detailed results to output_test_results.json...")
    default_data = create_mock_student_data()
    full_result = generate_learning_path(
        student_profile=default_data["student_profile"],
        academic_data=default_data["academic_data"],
        psychology_data=default_data["psychology_data"],
        timetable=default_data.get("timetable"),
        report_card=default_data.get("report_card"),
        study_habits=default_data.get("study_habits"),
    )

    with open("output_test_results.json", "w", encoding="utf-8") as f:
        json.dump(full_result, f, indent=2, default=json_serializer, ensure_ascii=False)

    print("Done!")


if __name__ == "__main__":
    main()
