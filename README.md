# Camcom.ai problem statement solution

Problem statement: 

There is a manual QC process which happens. 
There is a portal from which each individual qc task is assigned. 
The portal needs to check how many qc persons are logged in and which of the logged in persons are free, as in not on a task, and automatically assign tasks. 
Once the task is finished the person will automatically get assigned the next task if any is pending. 
How would you architect this?
I want to understand step by step the methodology you used to come to the final solution. Illustrate a basic API framework written in Python using Flask and MySql as the database.


Solution: 

There are 3 major components written in the solution, they are as: 

1. TaskCommandService: Marks tasks as completed and assigns unassigned tasks to users.

2. Scheduled background cron job: Scheduled as per our chosen time, it will fetch all logged-in and free users and will feed them to TaskCommandService's assign_unassigned_tasks() function.

3. API's: logged-in/ : This will mark a user as logged in.task/marked-completed: This will mark the user's task as completed and will make the user's status as is_free = True after which this user will be fed to TaskCommandService() to assign it a new unassigned task.


This solution proposes that any free user will be assigned a task as soon as the background scheduled task runs and also when a user's task is completed he will automatically be assigned to a pending unassigned task. This will ensure no tasks remain unassigned.
