"""Module contains the view functions for employees."""
from datetime import datetime

import requests as client
from flask import render_template, request, redirect, flash, abort, url_for

from department_app.forms import EmployeeForm, SearchEmployee
from department_app.views import bp

BASE_URL = "http://127.0.0.1:5000"


@bp.route('/employees', methods=['GET', 'POST'])
def view_employees_list():
    """
    On GET request obtains the list of employees from the REST-API and renders the
    "employees_list.html" template with form to create a new employee.
    On form submission validates the form data, if validation fails rerenders
    the template with error messages. If valid data send in in a post request to the REST-API.
    If it returns status code 201 redirects to self and flashes a success message,
    else flashes the API-sent error message.
    """
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments)
    search_form = SearchEmployee()
    if form.validate_on_submit():
        data = {
            'full_name': request.form['full_name'],
            'date_of_birth': request.form['date_of_birth'],
            'salary': request.form['salary'],
            'department_id': request.form['department_id']
        }
        response = client.post(f'{BASE_URL}/api/v1/employees', json=data)
        if response.status_code == 201:
            flash('New employee was created successfully', category='success')
            return redirect(url_for('views.view_employees_list'))
        flash(response.json()['message'], category='danger')
    employees = client.get(f'{BASE_URL}/api/v1/employees').json()
    return render_template(
        'employees_list.html',
        employees=employees,
        form=form,
        sform=search_form
    )


@bp.route('/employees/<int:emp_id>/delete')
def delete_employee(emp_id):
    """
    Performs a delete request to REST API with the employee wish emp_id.
    If response code is 404 aborts with 404 error.
    Else - redirects to departments_list_view with "deleted successfully"
    message.
    """
    employee = client.delete(f'{BASE_URL}/api/v1/employees/{emp_id}')
    if employee.status_code == 404:
        abort(404, description=employee.json()["message"])
    flash('Employee was deleted successfully', category='success')
    return redirect(request.referrer)


@bp.route('/departments/<int:dep_id>/employees', methods=['POST'])
def create_employee(dep_id):
    """
    Processes the form submission in "department_details.html", validates the date,
    if invalid - redirects back with validation errors. If valid adds to the data
    the department id and  posts it to the REST API. If response status code is 201 -
    redirects to department_detail view with success massage. Else redirects with error
    message and the prefilled form.
    """
    departments = client.get(f'{BASE_URL}/api/v1/departments').json()
    form = EmployeeForm(departments, request.form, department_id=dep_id)
    if form.validate_on_submit():
        data = {
            'full_name': request.form['full_name'],
            'date_of_birth': request.form['date_of_birth'],
            'salary': request.form['salary'],
            'department_id': dep_id
        }
        response = client.post(f"{BASE_URL}/api/v1/departments/{dep_id}/employees", json=data)
        if response.status_code == 201:
            flash('New employee was created successfully', category='success')
            return redirect(url_for('views.view_department_details', dep_id=dep_id))
        flash(response.json()['message'], category='danger')
    department = client.get(f'{BASE_URL}/api/v1/departments/{dep_id}').json()
    return render_template(
        'department_details.html',
        department=department,
        employees=department['employees'],
        form=form
    )


@bp.route('/employees/<int:emp_id>/edit/<int:from_dep>', methods=['GET', 'POST'])
def edit_employee(emp_id, from_dep=0):
    """
    On GET request renders the "employees_list.html" template with
    form filled with data of the employee to edit, if invalid emp_id
    specified in url - aborts with 404 error. On form submitting validates
    the data. If validation passes - PUTs data to REST API. If response code
    is 200 redirects  with success message. Else - with error message and filled
    form. The redirect point to employees list view or to a department detail
    view, depending on where the "Edit" was requested.
    """
    response = client.get(f"{BASE_URL}/api/v1/employees/{emp_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    response_data = response.json()
    response_data["date_of_birth"] = datetime.strptime(
        response_data["date_of_birth"], "%Y-%m-%d"
    ).date()
    response_data["department_id"] = response_data["department"]["id_"]
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments, data=response_data)
    if form.validate_on_submit():
        data = {
            "full_name": request.form["full_name"],
            "date_of_birth": request.form["date_of_birth"],
            "salary": request.form["salary"],
            "department_id": response_data["department_id"],
        }
        response = client.put(f"{BASE_URL}/api/v1/employees/{emp_id}", json=data)
        if response.status_code == 200:
            flash("Employee updated successfully.", category='success')
            return (
                redirect(url_for("views.view_employees_list")) if from_dep == 0 else
                redirect(url_for("views.view_department_details", dep_id=data["department_id"]))
            )
        flash(response.json()["message"], category='danger')
    department = client.get(
        f'{BASE_URL}/api/v1/departments/{response_data["department_id"]}'
    ).json()
    if from_dep:
        return render_template(
            'department_details.html',
            department=department,
            employees=department['employees'],
            emp_id=emp_id,
            form=form,
            action='edit',
            from_dep=from_dep
        )
    employees = client.get(f'{BASE_URL}/api/v1/employees').json()
    return render_template(
        'employees_list.html',
        employees=employees,
        form=form,
        action='edit',
        emp_id=emp_id
    )


@bp.route('/departments/<int:dep_id>/employees/search')
@bp.route('/employees/search')
def search_employees(dep_id=None):
    """
    Gets the "date_of_birth" and "date_for_interval"(if provided) query
    parameters and makes a request to the REST API with them. Renders the
    "department_detail.html" or "employees_list.html" template (depending on
    where is called from) with the list of employees obtained from API.
    If invalid dep_id specified in url - aborts with 404 error.
    """
    date_of_birth = request.args.get('date_of_birth')
    date_for_interval = request.args.get('date_for_interval')
    if dep_id:
        response = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
        if response.status_code == 404:
            abort(404, description=response.json()["message"])
        url = f'&date_for_interval={date_for_interval}'
        employees = client.get(
            f"{BASE_URL}/api/v1/departments/{dep_id}/employees/search?date_of_birth={date_of_birth}{url if date_for_interval else ''}"
        )
        return render_template(
            'department_details.html',
            employees=employees.json(),
            action='search_result',
            department=response.json()
        )
    url = f'&date_for_interval={date_for_interval}'
    employees = client.get(
        f"{BASE_URL}/api/v1/employees/search?date_of_birth={date_of_birth}{url if date_for_interval else ''}"
    )
    return render_template(
        'employees_list.html',
        employees=employees.json(),
        action='search_result'
    )
