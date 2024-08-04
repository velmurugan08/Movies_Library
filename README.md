Movie Library

Overview

Movie Library is a web application where users can search for movies, view details, and create lists of their favorite movies. Users can create multiple movie lists (similar to YouTube playlists) and choose to make them either public or private. Public lists can be shared with anyone using a link, while private lists are only visible to the creator.
Features

* User Authentication: Sign In/Sign Up functionality.
* Movie Search: Search for movies using the OMDB API and view movie details.
* Movie Lists: Create and manage lists of movies.
* Responsive Design: An intuitive and attractive user interface.

Steps to Start the Application
Clone the Repository

bash

    git clone https://github.com/velmurugan08/Movie_Library.git

    cd Movie_Library

Create and Configure the .env File

Create a .env file based on the .env.example file provided in the repository. Fill in the necessary environment variables.
Create a Virtual Environment

bash

    python3 -m venv venv

Activate the Virtual Environment

For Linux/macOS:

bash

    source venv/bin/activate

For Windows:

bash

    venv\Scripts\activate

Install Requirements

bash

    pip install -r requirements.txt

Migrate the Database

bash

    python3 manage.py migrate

Run the Application

bash

    python3 manage.py runserver

Tech Stack Used

* Django: For developing the website.
* PostgreSQL: For database management.
* HTML, CSS, and JavaScript: For front-end development.
* Amazon AWS: For hosting the application and managing the database.
* Onrender: The website is hosted in live using the onrender provider.

Live Demo

The application is hosted online. You can access it here.
live link :

    https://movie-library-vhhq.onrender.com

If you want to contribute to this project, please follow these steps:

* Fork the repository.
* Create a new branch (git checkout -b feature-branch).
* Make your changes and commit them (git commit -am 'Add some feature').
* Push to the branch (git push origin feature-branch).
* Create a new Pull Request.

License

This project is licensed under the MIT License.

Feel free to explore the application and provide any feedback. Happy movie listing!

By: Velmurugan08
