from django.test import TestCase
from django.contrib.auth.models import Group

from constants import MANAGER, SALES, SUPPORT
from core.models import Employee

# Create your tests here.


class EmployeeTestCase(TestCase):
    def setUp(self):

        Group.objects.get_or_create(id=1, name="Management")
        Group.objects.get_or_create(id=2, name="Sales")
        Group.objects.get_or_create(id=3, name="Support")

        Employee.objects.get_or_create(username="mpotel", first_name="Martin", last_name="Potel",
                                       email="martin.potel@epicteam.com", phone="0033164752546")
        management = Group.objects.filter(name='Management').first()
        Employee.objects.filter(username="mpotel").first().groups.add(management)

        Employee.objects.get_or_create(username="lprevosteau", first_name="Louis", last_name="Prevosteau",
                                       email="louis.prevosteau@epicteam.com", phone="0033164753974")
        sales = Group.objects.filter(name='Sales').first()
        Employee.objects.filter(username="lprevosteau").first().groups.add(sales)

        Employee.objects.get_or_create(username="prognon", first_name="Pierre", last_name="Rognon",
                                       email="pierre.rognon@epicteam.com", phone="0033164757464")
        support = Group.objects.filter(name='Support').first()
        Employee.objects.filter(username="prognon").first().groups.add(support)

        Employee.objects.get_or_create(first_name="Nicolas", last_name="Journet",
                                       email="nicolas.journet@epicteam.com", phone="0033164757561")

    def test_employee_get_group(self):
        """
        Employee's department is returned
        """
        martin = Employee.objects.filter(first_name="Martin").first()
        louis = Employee.objects.filter(first_name="Louis").first()
        pierre = Employee.objects.filter(first_name="Pierre").first()
        self.assertEqual(martin.department.id, MANAGER)
        self.assertEqual(louis.department.id, SALES)
        self.assertEqual(pierre.department.id, SUPPORT)

    def test_employee_get_group_no_group(self):
        """
        Employee not affected to a department should return "(Not affected yet)"
        """
        nicolas = Employee.objects.get(first_name="Nicolas")
        self.assertEqual(nicolas.department, '(Not affected yet)')
