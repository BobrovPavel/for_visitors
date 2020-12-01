import time
from requests import ReadTimeout
from src.framework.logger import logger
from src.commons.constants import REQUEST_TIME_LIMIT
from src.framework.requests.students import StudentRequests
from src.exceptions.api_exceptions import StudentNotFoundException, StudentNotCreatedException

logger = logger.get_logger()
api = StudentRequests()


class Students:
    @staticmethod
    def number_of_students(subdomain, *, api_key, server):
        return len(api.get_students_list(subdomain, api_key=api_key, server=server))

    @staticmethod
    def create(subdomain, email, *args, api_key, server):
        student_detail = subdomain, email, *args
        logger.info(f"Create user on the {subdomain}. \nDetails: {student_detail}")
        try:
            return api.create_student(*student_detail, api_key=api_key, server=server)
        except ReadTimeout:
            logger.info(f"Failed to create student in 10 seconds: {student_detail}")
            raise StudentNotCreatedException(f"Failed to create student in 10 seconds: {student_detail}")

    @staticmethod
    def get_assigned_dashboards(subdomain, email, *, api_key, server):
        return Students().get_detail(subdomain, email, api_key=api_key, server=server)["dashboards"]

    @staticmethod
    def get_detail(subdomain, email, *, api_key, server):
        student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
        if email in student.values():
            return student
        else:
            logger.info(f"Student with email: {email} not found in subdomain: {subdomain}")
            raise StudentNotFoundException(f"subdomain = {subdomain}, email = {email}")

    @staticmethod
    def get_list(subdomain, *, api_key, server):
        try:
            return api.get_students_list(subdomain, api_key=api_key, server=server)
        except ReadTimeout:
            logger.info(f"Failed to get students list for: {subdomain}")
            raise StudentNotFoundException(f"Failed to get students list for: {subdomain} in 10 seconds")

    @staticmethod
    def wait_for_created(subdomain, email, *args, api_key, server):
        end_time = time.time() + REQUEST_TIME_LIMIT

        if args:
            student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
            while True:
                result = [email in student.values()]
                for arg in args:
                    result.append(arg in student.values())
                student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
                if all(result):
                    break
                if time.time() > end_time:
                    logger.info(f"Failed to create student: {email} in subdomain: {subdomain}")
                    raise TimeoutError(f"Failed to create student: subdomain = {subdomain}, email = {email}")
        else:
            student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
            while email not in student.values():
                student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
                if time.time() > end_time:
                    logger.info(f"Failed to create student: {email} in subdomain: {subdomain}")
                    raise TimeoutError(f"Failed to create student: subdomain = {subdomain}, email = {email}")

    @staticmethod
    def delete_by_email(subdomain, email, *, api_key, server):
        logger.info(f"Delete user by email: {subdomain}, {email}")
        end_time = time.time() + REQUEST_TIME_LIMIT
        student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
        if email in student.values():
            api.delete_student(subdomain, email, api_key=api_key, server=server)
            while email in student.values():
                student = api.get_student_details(subdomain, email, api_key=api_key, server=server)
                if time.time() > end_time:
                    logger.info(f"Failed to delete student: {email} in subdomain: {subdomain}")
                    raise TimeoutError(f"Failed to delete student: subdomain = {subdomain}, email = {email}")
        else:
            logger.info(f"Student with email: {email} not found in subdomain: {subdomain}")
            raise StudentNotFoundException(f"subdomain = {subdomain}, email = {email}")

    @staticmethod
    def delete_all(subdomain, *, api_key, server):
        logger.info(f"Delete all students from {subdomain}")
        end_time = time.time() + REQUEST_TIME_LIMIT
        while api.get_students_list(subdomain, api_key=api_key, server=server):
            for student in api.get_students_list(subdomain,api_key=api_key, server=server):
                Students().delete_by_email(subdomain, student["email"], api_key=api_key, server=server)
                if time.time() > end_time:
                    logger.info(f"Failed to delete all students in subdomain: {subdomain}")
                    raise TimeoutError(f"Failed to delete all students students:in subdomain: {subdomain}")
