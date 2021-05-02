# activeEdgeAPI
a simple api collection that allows for the creation, read, update, and deletion of employees in a database


GET http://127.0.0.1:8000/employees/?first_name__icontains=&last_name__icontains=
POST http://127.0.0.1:8000/employees/
{
    "first_name" : "Peter",
    "last_name": "Griffin",
    "date_of_birth": "1992-01-01"
}
GET http://127.0.0.1:8000/employee/<int:employee_id>
PUT http://127.0.0.1:8000/employee/<int:employee_id>
DELETE http://127.0.0.1:8000/employee/<int:employee_id>
