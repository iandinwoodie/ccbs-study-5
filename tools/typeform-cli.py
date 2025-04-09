#!/usr/bin/env python3

# Standard library imports
import argparse
import os
import json
import pathlib

# Third-party library imports
import typeform


class Typeform:

    TITLES = [
        "house-soiling-study-owner",
        "house-soiling-study-dog",
        "house-soiling-study-dog-inner-loop",
        "house-soiling-study-next-dog-redirect",
    ]

    def __init__(self, api_key: str, forms_dir: pathlib.Path):
        self.tf = typeform.Typeform(token=api_key)
        if not self.tf:
            raise ValueError("Failed to create Typeform client.")
        self.forms_dir = forms_dir

    def push_forms(self):
        print("Pushing forms to Typeform...")

    def pull_forms(self):
        print("Pulling forms from Typeform...")
        forms: dict = self.tf.forms.list()
        pages = forms.get("page_count")
        ids = {}
        for i in range(pages):
            forms = self.tf.forms.list(page=i + 1)
            for form in forms["items"]:
                if form.get("title") in self.TITLES:
                    ids[form.get("title")] = form.get("id")

        # Create the forms directory if it doesn't exist.
        if not self.forms_dir.exists():
            self.forms_dir.mkdir(parents=True)

        for title, id in ids.items():
            print(f"Pulling form: {title}")
            form = self.tf.forms.get(uid=id)
            form_json = json.dumps(form, indent=2)
            form_path = self.forms_dir / f"{title}.json"
            with open(form_path, "w") as f:
                f.write(form_json)

    def pull_responses():
        print("Pulling responses from Typeform...")


def get_script_dir() -> pathlib.Path:
    """Returns the directory of the current script."""
    return pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


def get_forms_dir() -> pathlib.Path:
    """Returns the directory where forms are stored."""
    return get_script_dir().parent / "forms"


def main():
    parser = argparse.ArgumentParser(description="Typeform CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pull-forms", action="store_true", help="Pull forms from Typeform")
    group.add_argument("--push-forms", action="store_true", help="Push forms to Typeform")
    group.add_argument("--pull-responses", action="store_true", help="Pull responses from Typeform")
    args = parser.parse_args()

    api_key = os.getenv("TYPEFORM_API_KEY")
    if not api_key:
        raise ValueError("TYPEFORM_API_KEY environment variable is not set.")
    tf = Typeform(api_key=api_key, forms_dir=get_forms_dir())

    if args.pull_forms:
        tf.pull_forms()
    elif args.push_forms:
        tf.push_forms()
    elif args.pull_responses:
        tf.pull_responses()


if __name__ == "__main__":
    main()
