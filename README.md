# mailer-service
A mailer service that sends out text emails. The service utilizes SMTP server to send out emails. 

- For app itself, I personally used Sendgrid's SMTP server.
- For testing purposes, I used mailhog to simulate SMTP server.

As this service is pretty small and Pydantic handled most validation, dependecies and custom exceptions were omitted.
