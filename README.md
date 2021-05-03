# activeEdgeAPI
a simple api collection that allows for the creation, read, update, and deletion of employees in a database


## API ARCHITECTURE
The api's are built using python **django** rest framework with **postgresql** database for persistent storage of data  
The api's are hosted on heroku.com  
The api's support pagination, filtering, and authentication
Below is the employee table schema


### **EMPLOYEE SCHEMA**
```python
    class Employee(models.Model):

        first_name = models.CharField(max_length=1000)  # holds the employee first name its a character field
        last_name = models.CharField(max_length=1000)  # holds the employee last name its a character field
        date_of_birth = models.DateField() # holds the employee date of birth its a date field, used to dynamically derive the employees age
        join_date = models.DateTimeField(auto_now_add=True) # holds the date time that the employeed record was created, its a date time field
        created_by = models.CharField(max_length=1000, default="") # a control field to keep track of who created an employee
        created_on = models.DateTimeField(auto_now_add=True) # a control field to keep of when an employee was created
        last_updated_by = models.CharField(max_length=1000, default="") # a control field to keep track of who last edited an employee
        last_updated_on = models.DateTimeField(auto_now=True) #  a control field to keep track of when last an employee was updated
        
        # Note: an assumption was made that an emplpoyee's join date, is the date they were created in the database.
```
    
below are details of each api

## AUTHENTICATION  
*all the endpoints are protected, and hence require authentication to access*  
url: *https://activeedgeapi.herokuapp.com/api-auth/login/*  
username: ace  
password: admin  
after a successful login, you will be redirected to django default browsable api interface in the browser
from here the user can test the api's can be tested similar to postman.
*more info can be found at this link: [Django browsable api interface!](https://www.django-rest-framework.org/topics/browsable-api/)*



## CREATE EMPLOYEE  
*creates and employee and records and stores it to the database*  
url: *https://activeedgeapi.herokuapp.com/employees/*  
method: **POST**  
payload:  
```python
{
    "first_name" : "Peter",
    "last_name": "Griffin",
    "date_of_birth": "1992-01-01"
}
```
return a success message, 200, if successful  

## GET EMPLOYEES
*gets employees from the database, this endpoint is paginated and supports filtering*  
*the query params to filter by first name and last name are first_name__icontains, last_name__icontains respectively*
url: *https://activeedgeapi.herokuapp.com/employees/?first_name__icontains=joy&last_name__icontains=*  
method: **GET**  
payload: no payload  
return a success message, 200, if successful  


## GET A SINGLE EMPLOYEE
*gets a single employee from the database*  
*requires the employee_id without the leading zeros, to be passed to the url, i.e if the employee id is 00001, only the number 1 should be passed to the url*  
url: *https://activeedgeapi.herokuapp.com/employee/<employee_id>*  
method: **GET**  
return a success message, 200 if successful


## UPDATE A SINGLE EMPLOYEE
*gets a single employee from the database*  
*requires the employee_id without the leading zeros, to be passed to the url, i.e if the employee id is 00001, only the number 1 should be passed to the url*  
url: *https://activeedgeapi.herokuapp.com/employee/<employee_id>*  
method: **PUT**  
return a success message, 200 if successful  

note: the fields that can be updated, are first_name, last_name, date_of_birth, but only fields you want to update need to be passed in the JSON payload, example
if you wish to update only first_name, you can pass in only first name without passing in the other fields as shown below: 
```python
    {
        "first_name": "new first name"
    }
```
but if you wish to update all fields you can pass in all the fields
```python
    {
        "first_name": "new first name",
        "last_name": "new last name",
        "date_of_birth": "new date of birth with format YYYY/MM/DD"
    }
```


## DELETE A SINGLE EMPLOYEE
*gets a single employee from the database*  
*requires the employee_id without the leading zeros, to be passed to the url, i.e if the employee id is 00001, only the number 1 should be passed to the url*  
url: *https://activeedgeapi.herokuapp.com/employee/<employee_id>*  
method: **DELETE**  
return a success message, 200 if successful

note: a 404 is always returned, anytime an employee id is not found in the database. 
