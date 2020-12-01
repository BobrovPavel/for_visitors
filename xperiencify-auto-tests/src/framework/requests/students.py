import pytest
import requests
from src.commons.constants import first_name_default, last_name_default, password_default
from src.commons.constants import ORDER_FORM_API_KEY


def create_student_url(subdomain, api_key, server):
    return f"https://{subdomain}.xperiencify.{server}/api/v4/students/?api_key={api_key}"


def delete_student_url(subdomain, api_key, server):
    return f"https://{subdomain}.xperiencify.{server}/api/v4/student/delete/?api_key={api_key}"


def student_details_url(subdomain, api_key, server):
    return f"https://{subdomain}.xperiencify.{server}/api/v4/student/detail/?api_key={api_key}"

def students_list_url(subdomain, api_key, server):
    return f"https://{subdomain}.xperiencify.{server}/api/v4/students/?api_key={api_key}"


class StudentRequests:

    @staticmethod
    def create_student(subdomain, email, fname=first_name_default, lname=last_name_default, password=password_default, *, api_key, server):
        data = ({
            "api_key": api_key,
            "first_name": fname,
            "last_name": lname,
            "email": email,
            "password": password
        })

        return requests.post(create_student_url(subdomain, api_key, server), data, timeout=10).json()

    @staticmethod
    def delete_student(subdomain, email, *, api_key, server):
        data = ({
            "api_key": api_key,
            "domain": f"{subdomain}.xperiencify.{server}",
            "email": email
        })

        requests.post(delete_student_url(subdomain, api_key, server), data)

    @staticmethod
    def get_student_details(subdomain, email, *, api_key, server):
        data = ({
            "api_key": ORDER_FORM_API_KEY,
            "domain": f"{subdomain}.xperiencify.dev",
            "email": email
        })

        return requests.post(student_details_url(subdomain, api_key, server), data).json()

    @staticmethod
    def get_students_list(subdomain, *, api_key, server):
        data = ({
            "api_key": api_key,
        })
        return requests.get(students_list_url(subdomain, api_key, server), data, timeout=10).json()
