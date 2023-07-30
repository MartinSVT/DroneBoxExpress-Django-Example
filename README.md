# DroneBoxExpress
Django Project Example - for testing purposes only

The project is currently being developed and it’s not in its finished state 

Current Status: Functionality Completed, front-end in development 

The web project is of an imaginary company for delivering packages using drones and predetermined routes, the idea is that the web application has multiple functionalities and acts as both customer platform and staff/operational platform. Depending on the profile type that is currently logged in, the web application either acts as a platform to add new airports, drones, routes, articles and also completes and cancels automatically generated flights or act as a customer platform where information can be viewed and individual orders can be placed, modified and deleted. The web application notifies the user for changes to his/her orders status via email. The application also keep track of total profits revenue and expenses, where once a flight is completed its orders are added to the company revenue and the flight expenses are calculated using the distance, fuel burn rate, fuel price, operational cost of the selected airports etc… once calculated the total profit revenue and expenses are help in the DB for statistical purposes.
There are 4 profile types in the application and 3 user types all of which are handled via custom user and profile models and their associated signals

Profiles Types
1.	Admin
2.	Editor
3.	Pilot
4.	Customer
   
User Types
1.	Superuser
2.	Staff
3.	Normal
   
These are the following sections the Web application has:

•	Home Section – Displaying recently added articles, news and events from the company staff, if a staff user is logged in it allows it to create new articles and modify and delete articles, he/she has created.

•	Contacts and about us – Displaying company information 

•	Profile Section – allowing a logged user to view, edit and delete his/her profile 

•	Operations Section – Allowing a user with a profile of Pilot to make CRUD operation over the existing Airport, Drones, Routes and Flights. It also allows to complete and cancel flights that are assigned to the given pilot

•	Orders Section – Allows customers to generate orders, modify them and delete them if not scheduled or completed. If user is Editor(staff) it allows further functionality to adjust current price ranges and available discounts via JS and Django REST API
