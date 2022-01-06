"""Module contains the view functions for departments."""
import requests as client
from flask import render_template, request, redirect, flash, url_for, abort

from department_app.forms import DepartmentForm, EmployeeForm, SearchEmployee
from department_app.views import bp

BASE_URL = "http://127.0.0.1:5000"


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/departments', methods=['GET', 'POST'])
def departments_list_view():
    """
    On GET request obtains the list of departments from the REST-API and renders the
    "departments_list.html" template with form to create a new department.
    On form submission validates the form data, if validation fails rerenders
    the template with error messages. If valid data send in a post request to the REST-API.
    If it returns status code 201 redirects to self and flashes a success message,
    else flashes the API-sent error message.
    """
    form = DepartmentForm()
    if form.validate_on_submit():
        data = {'title': request.form['title']}
        response = client.post(f'{BASE_URL}/api/v1/departments', json=data)
        if response.status_code == 201:
            flash('Department created successfully.', category='success')
        else:
            flash(response.json()['message'], category='danger')
        return redirect(url_for('views.departments_list_view'))
    departments = client.get(f'{BASE_URL}/api/v1/departments').json()
    return render_template(
        'departments_list.html',
        departments=departments,
        form=form,
        active='departments'
    )


@bp.route('/departments/<dep_id>')
def view_department_details(dep_id):
    """
    Renders the "department_details.html" template, with the list of employees
    working in the specified department and a form to add employees to it.
    If invalid dep_id passed in the url - aborts with 404 error.
    """
    sform = SearchEmployee()
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments)
    department = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
    if department.status_code == 404:
        abort(404, description=department.json()["message"])
    department = department.json()
    return render_template(
        'department_details.html',
        department=department,
        employees=department['employees'],
        form=form,
        sform=sform
    )


@bp.route('/departments/<dep_id>/edit', methods=['GET', 'POST', 'PUT'])
def edit_department(dep_id):
    """
    On GET request renders the "departments_list.html" template with
    form filled with data of the department to edit, if invalid dep_id
    specified in url - aborts with 404 error. On form submitting validates
    the data. If validation passes - PUTs data to REST API. If response code
    is 200 redirects to departments_list_view with success message. Else -
    with error message and filled form.
    """
    response = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    form = DepartmentForm(data=response.json())
    if form.validate_on_submit():
        data = {"title": request.form["title"]}
        if data['title'] == response.json()['title']:
            flash("Department name should be different from previous one.", category='danger')
            return redirect(url_for("views.edit_department", dep_id=dep_id))
        response = client.put(f"{BASE_URL}/api/v1/departments/{dep_id}", json=data)
        if response.status_code == 200:
            flash("Department updated successfully.", category='danger')
            return redirect(url_for("views.edit_department", dep_id=dep_id))
        flash(response.json()["message"], category='danger')
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    return render_template(
        "departments_list.html",
        department=response.json(),
        action="edit",
        form=form,
        departments=departments
    )


@bp.route('/departments/<dep_id>/delete')
def delete_department(dep_id):
    """
    Performs a delete request to REST API with the department id.
    If response code is 404 aborts with 404 error.
    Else - redirects to departments_list_view with "deleted successfully"
    message.
    """
    response = client.delete(f'{BASE_URL}/api/v1/departments/{dep_id}')
    if response.status_code == 404:
        abort(404, description=response.json()['message'])
    else:
        flash('Department deleted successfully.', category='success')
    return redirect(url_for('views.departments_list_view'))


@bp.route('/about')
def about():
    """Renders template with info about project."""
    return render_template('about.html')
