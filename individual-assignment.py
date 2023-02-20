import requests
import json

# Set the URL and header for the API request
url = "https://yourcanvasinstance.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/update_grades"
headers = {
    "Authorization": "Bearer {access_token}",
    "Content-Type": "application/json"
}

# Set the grades data
grades = {
    "grade_data": [
        {
            "student_id": "{student_id_1}",
            "posted_grade": "{grade_1}"
        },
        {
            "student_id": "{student_id_2}",
            "posted_grade": "{grade_2}"
        },
        # Add more grades as needed
    ]
}

# Convert grades data to JSON format
grades_json = json.dumps(grades)

# Make the API request
response = requests.post(url, headers=headers, data=grades_json)

# Check if the request was successful
if response.status_code == 200:
    print("Grades were successfully updated!")
else:
    print("There was an error updating the grades.")
    print("Response code:", response.status_code)
    print("Response message:", response.text)

