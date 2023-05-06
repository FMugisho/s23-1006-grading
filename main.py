import argparse
import csv
import sys
from pathlib import Path
from typing import List
import requests

access_token = ""
course_id = ""
assignment_id = ""
input_file_path = ""
is_group = False

api_url = "https://courseworks2.columbia.edu/api/v1"
headers = {"Authorization": f"Bearer {access_token}"}
submission_url = f"{api_url}/courses/{course_id}/assignments/{assignment_id}/submissions/update_grades"


def parse_arguments():
    global access_token, course_id, assignment_id, input_file_path, is_group
    parser = argparse.ArgumentParser(description="Update grades on Canvas.")
    parser.add_argument(
        "-t", "--access-token", required=True, help="Canvas API access token."
    )
    parser.add_argument("-c", "--course-id", required=True, help="Canvas course ID.")
    parser.add_argument(
        "-a", "--assignment-id", required=True, help="Canvas assignment ID."
    )
    parser.add_argument(
        "-f", "--input-file-path", required=True, help="Path to input CSV file."
    )
    parser.add_argument(
        "-g",
        "--is-group",
        action="store_true",
        help="Indicates whether the assignment was done in group or not.",
    )

    args = parser.parse_args()
    access_token = args.access_token
    course_id = args.course_id
    assignment_id = args.assignment_id
    input_file_path = args.input_file_path
    is_group = args.is_group

    headers["Authorization"] = f"Bearer {access_token}"
    submission_url = f"{api_url}/courses/{course_id}/assignments/{assignment_id}/submissions/update_grades"


def validate_config():
    if not access_token:
        raise ValueError("Invalid access token! It cannot be empty.")
    if not course_id:
        raise ValueError("Missing course ID! It cannot be empty.")
    if not assignment_id:
        raise ValueError("Missing assignment ID! It cannot be empty.")
    if not input_file_path:
        raise ValueError("Missing input file path! It cannot be empty.")
    if not isinstance(is_group, bool):
        raise ValueError(
            "Invalid value for is_group! It should be True or False to indicate whether the assignment was done in group or not."
        )
    if not Path(input_file_path).is_file():
        raise ValueError("The specified file does not exist.")


def validate_csv(reader, is_group: bool):
    headers = next(reader)
    required_headers = (
        ["Group ID", "Grades", "Comments"]
        if is_group
        else ["Student ID", "Grades", "Comments"]
    )

    if headers != required_headers:
        raise ValueError(
            f"Invalid CSV format. Expected headers: {', '.join(required_headers)}"
        )

    for row_number, row in enumerate(reader, start=2):
        if len(row) != len(required_headers) or any(cell == "" for cell in row):
            raise ValueError(
                f"Invalid CSV format. Null values found in row {row_number}."
            )


def get_group_members(group_id: str) -> List[str]:
    members_url = f"{api_url}/groups/{group_id}/users"
    response = requests.get(members_url, headers=headers)
    members = [member["id"] for member in response.json()]
    return members


def process_individual(reader):
    for student_id, grade, comment in reader:
        grade_data = {
            student_id: {
                "posted_grade": grade,
                "text_comment": comment.replace(";", " "),
                "group_comment": False,
            }
        }
        response = requests.post(
            submission_url, json={"grade_data": grade_data}, headers=headers
        )
        if response.status_code != 200:
            sys.stderr.write(f"Unable to post grades because {response.text}\n")
            sys.exit(1)
        else:
            sys.stdout.write(
                f"Uploaded grades for {student_id} who got {grade}% and comment {comment}\n"
            )


def process_group(reader):
    for group_no, group_id, grade, comment in reader:
        member_ids = get_group_members(group_id)
        for member_id in member_ids:
            grade_data = {
                str(member_id): {
                    "posted_grade": int(grade),
                    "text_comment": comment.replace(";", " "),
                    "group_comment": True,
                }
            }
            response = requests.post(
                submission_url, json={"grade_data": grade_data}, headers=headers
            )
            if response.status_code != 200:
                sys.stderr.write(f"Unable to post grades because {response.text}")
                sys.exit(1)
            else:
                sys.stdout.write(
                    f"Uploaded grades for {member_id} from group {group_no} who got {grade}% and comment {comment}\n"
                )


def main():
    validate_config()
    with open(input_file_path, mode="r") as input_file:
        reader = csv.reader(input_file)
        validate_csv(reader, is_group)

        if is_group:
            process_group(reader)
        else:
            process_individual(reader)


if __name__ == "__main__":
    parse_arguments()
    main()
