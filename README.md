## Urban Style
### This is a Django e-commerce website powered by Stripe library to provide convenient access to the Stripe API from applications written in the Python language. Its main function is to take full advantage of the custom models - users, categories and products, to make it possible for the vendors to add merchandise, create accounts and log in.

--------------------------------------------------

### Features:
* Using Bulma CSS framework to implement its built-in frontend components
* Working with template inheritance mechanism to build a base “skeleton” template that contains all the common elements and defines blocks that child templates can override
* Implementing secure user authentication system which handles user accounts, manages cookies, user groups, and sessions, and keeps track of permissions
* Taking full advantage of Django's built-in features like cross-site request forgery protection to ensure safe data transfer in web forms to a database
* Associating multiple records in a table with multiple records in another table ( many-to-many relationship ) to achieve optimal ORM performance
* Breaking logic into smaller parts by adding various new Django applications to an existing project 
* Writing as much functionality as possible in models or utility files instead of views 
* Serving static files with WhiteNoise to accomplish high performance and efficiency without depending on nginx, Amazon S3 or any other external service
* Relying on Cloudinary to provide a secure and comprehensive API for easily uploading media files from server-side code
* Storing app’s secure credentials in environment variables
* Utilizing setUpModule() to handle especially expensive setup operations for all of the tests within a module
* Performing extensive selenium tests using 'page object pattern' instead of making raw WebDriver calls to have cleaner code:
  * Utilizing DRY (Don’t repeat yourself) principle to minimize code duplication by having all ID-locators in one place
  * Setting an interface between web page’s elements and tests
  * Avoiding usage of WebDriver APIs in test methods
  * Encapsulating the services of web pages, not only exposing their elements

--------------------------------------------------

### Docker info:
* Pull an image from my Docker Hub - click on the icon below
* Create and start a container 
* Pass environment variables to your container
  * with the -e flag or using .env file

```
docker run -p 8000:8000 -e STRIPE_PUB_KEY="<your stripe public key>" -e STRIPE_SECRET_KEY="<your stripe secret key>" -e EMAIL_HOST_USER="<your email host user>" -e EMAIL_HOST_PASSWORD="<your email host password>" <imagename>

```
```
docker run -p 8000:8000 --env-file .env <imagename>

```

--------------------------------------------------

### Code Coverage:
* Selenium and unit tests combined

```
coverage run -p manage.py test unit_tests && coverage run -p manage.py test selenium_tests && coverage combine && coverage html

```

<img src="https://github.com/mjaroszewski1979/django-eshop-v2/blob/main/cov_html_report.png">

------------------------------------------------


![caption](https://github.com/mjaroszewski1979/django-eshop-v2/blob/main/urban_style.gif)
  
  Live | Code | Docker | Technologies
  ---- | ---- | ------ | ------------
  [<img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/heroku_g.png">](https://django-eshop-v1.herokuapp.com/) | [<img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/github_g.png">](https://github.com/mjaroszewski1979/django-eshop-v2) | [<img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/docker_g.png">](https://hub.docker.com/r/maciej1245/urbanstyle) | <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/python_g.png"> &nbsp; <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/django_g.png"> &nbsp;  <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/html_g.png"> <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/css_g.png"> &nbsp; <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/bulma_g.png"> &nbsp; &nbsp; <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/js1.png"> &nbsp; &nbsp; <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/stripe.png"> &nbsp; &nbsp; <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/cloudinary.png">



