# Python E1006 Canvas Grade Uploader

This tool has been developed as part of Python E1006 at Columbia University to help grade assignments on Canvas. It reads grades and comments from a CSV file and uploads them to Canvas using the API.

## Installation

Make sure you have Python 3.6 or higher installed.

## Usage

1. Set up an access token on Canvas:
   - Log in to Canvas and navigate to your "Account" settings.
   - Click "New Access Token" and provide a name and expiration date for the token.
   - Copy the generated access token.

2. Find the course ID and assignment ID on Canvas:
   - Navigate to the assignment on Canvas.
   - Look at the URL in your browser's address bar. It should have the following format: `https://<your_canvas_domain>/courses/<course_id>/assignments/<assignment_id>`
   - Copy the `<course_id>` and `<assignment_id>` values.

3. Prepare a CSV file with the required format:
   - For group assignments, the CSV file should have the following fields: `Group ID, Grades, Comments`.
   - For individual assignments, the CSV file should have the following fields: `Student ID, Grades, Comments`.

4. Run the script with the following command line arguments:

```sh
python script_name.py --access-token your_access_token --course-id your_course_id --assignment-id your_assignment_id --input-file-path your_input_file_path [--is-group]
```

Replace `script_name.py` with the actual filename of your script, and provide the appropriate values for `your_access_token`, `your_course_id`, `your_assignment_id`, and `your_input_file_path`. Add the `--is-group` flag if it's a group assignment.

Example:

```sh
python canvas_grade_uploader.py --access-token abcd1234 --course-id 12345 --assignment-id 67890 --input-file-path group_grades.csv --is-group
```

## CSV File Format

### Group Assignments

The CSV file should have the following format:

```
Group ID, Grades, Comments
1, 85, Great work on the project!
2, 90, Excellent job, but there are a few areas for improvement.
...
```

### Individual Assignments

The CSV file should have the following format:

```
Student ID, Grades, Comments
123456, 95, Fantastic job on the assignment!
234567, 88, Good effort, but there's room for improvement.
...
```
## Note
This tool can work for any course at Columbia that uses Courseworks.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).
