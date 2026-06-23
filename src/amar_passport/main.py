#!/usr/bin/env python
import sys
import warnings

from crew import AmarPassport

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew with user profile inputs for Bangladesh E-Passport.
    """
    inputs = {
        'age': '24',
        'profession': 'private sector employee',
        'urgency': 'Express',
        'pages': '64',
        'location': 'Dhaka',
        'has_nid': 'Yes'
    }

    try:
        AmarPassport().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()
