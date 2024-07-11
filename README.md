# ProStats
![Project landing page](https://github.com/StarCodes2/ProStats/blob/main/image.png)

## Table of Contents

- [About](#about)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [Related projects](#-related-projects)
- [License](#-license)

## About
ProStats is a web application designed to help Project Managers, Contributors/Collaborators, and Open Source Maintainers create visualizations of activities on their project's GitHub repository. As a full-stack developer working on this project, my goal was to create an application that's easy to use and accessible on both mobile and web platforms.

This project was inspired by my experience as a student at ALX Africa. During the program, we needed to work in teams on various projects, with each team member responsible for a specific percentage of the commits to the project's repository. Tracking these commits became tedious, as GitHub only provides a bar chart showing the number of commits per contributor. I realized this could be improved, and with some research, I found that all the necessary data for better visualization is accessible through the GitHub RESTful API. This made choosing this project a no-brainer for me.
- [ProStats](https://prostats.pythonanywhere.com/)
- [Project Article](https://medium.com/@anu.ezekiel02/welcome-to-prostats-87f58bcd84ce)
- [Developer's Profile](https://www.linkedin.com/in/ezekiel-ogunewu)

## Installation

Follow these steps to install and set up the web application on an Ubuntu system.

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- `pip` (Python package installer)
- `virtualenv` (Optional but recommended for creating an isolated environment)

### Step 1: Update and Upgrade the System

First, make sure your package list is up to date and upgrade all your packages:

```bash
sudo apt update
sudo apt upgrade
```

### Step 2: Install Python and pip
If you don't have Python 3 and pip installed, you can install them using:

```bash
sudo apt install python3 python3-pip
```

### Step 3: Create a Virtual Environment (Optional but Recommended)
Creating a virtual environment helps manage dependencies and avoid conflicts with other Python projects. Install virtualenv if you haven't already:

```bash
sudo pip3 install virtualenv
```

Create and activate a virtual environment:

```bash
virtualenv venv
source venv/bin/activate
```

### Step 4: Clone the Repository
Clone the project repository from GitHub and setup the database:

```bash
git clone https://github.com/StarCodes2/ProStats.git
cd ProStats
cat setup_mysql_dev.sql | sudo mysql -u username -p
```

### Step 5: Install Dependencies
Install the required Python packages listed in the requirements.txt file:

```bash
pip3 install -r requirements.txt
```

## Usage
### Run the Application
Start the flask application:

```bash
MYSQL_USER=ps_user MYSQL_DB=pro_stat_dev_db MYSQL_HOST=localhost MYSQL_PWD=Password python3 -m app
```

### Access the Application
Open your web browser and navigate to:

```bash
http://127.0.0.1:5000
```

## Contributing
There are no guidelines for contributing to the project at this time.


## Related projects
- Augur is a Flask web application, Python library and REST server that presents metrics on open source software development project health and sustainability.
- Apache Kibble is a suite of tools for collecting, aggregating and visualizing activity in software projects.

## License
None

