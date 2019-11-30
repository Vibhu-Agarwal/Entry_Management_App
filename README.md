
<p align="center">
  <img src="./logo/logo.png" width="160">
</p>

# Entry Management App

[![Open Issues](https://img.shields.io/github/issues/Vibhu-Agarwal/Entry_Management_App?style=for-the-badge)](https://github.com/Vibhu-Agarwal/Entry_Management_App/issues) [![Forks](https://img.shields.io/github/forks/Vibhu-Agarwal/Entry_Management_App?style=for-the-badge)](https://github.com/Vibhu-Agarwal/Entry_Management_App/network/members) [![Stars](https://img.shields.io/github/stars/Vibhu-Agarwal/Entry_Management_App?style=for-the-badge)](https://github.com/Vibhu-Agarwal/Entry_Management_App/stargazers) ![Maintained](https://img.shields.io/maintenance/yes/2019?style=for-the-badge&logo=github)  ![Made with Django](https://img.shields.io/badge/Made%20with-Django-blueviolet?style=for-the-badge&logo=django)  ![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red?style=for-the-badge&logo=open-source-initiative)  ![Built with Love](https://img.shields.io/badge/Built%20With-%E2%99%A5-critical?style=for-the-badge&logo=ko-fi) 


## Index

- [Index](#index)
- [About](#about)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Gallery](#gallery)
- [Credit/Acknowledgment](#creditacknowledgment)
- [License](#license)

## About

Entry Management App is a web application that can be used at entry-points at several places, partcularly targetting offices where it needs to digitalize their process of maintaining records of visitors and visits. The application keeps the users updated about entry and exit of the visit through text messages and mails.

### Tech Stack Used
The application backed by Django framework and for its back-end and uses SQLite3 as database to store data. It also makes use of Twilio APIs to send SMS to Hosts of the Visit. The front-end of the application is written in HTML and CSS and uses AJAX calls with forms for auto-completion.

### Summer Geeks
The project is made for my submission for the [SummerGeeks 2020](https://summergeeks.in/) challenge.

## Usage

If you just want to do a simple test run of the application, just follow these steps:

- Clone the repository

```bash
$ git clone https://github.com/Vibhu-Agarwal/Entry_Management_App.git
```
- Install dependencies by using the following commands.

```bash
$ cd Entry_Management_App
$ pip install -r requirements.txt
```
```bash
$ cd event_manager
```
- Get credentials and a trial number [Twilio](www.twilio.com/referral/vqcjRB).
- Make sure 2FA is disabled on your mail account and [Less secure app access](https://myaccount.google.com/lesssecureapps) is turned on.

- Edit the values of variables in the `set_env_vars` file and save the changes.
```bash
export EM_EMAIL_HOST_USER="YOUR_(G)MAIL_ID"
export EM_EMAIL_HOST_PASSWORD="YOUR_(G)MAIL_PASSWORD"
export EM_TWILIO_ACCOUNT_SID="YOUR_TWILIO_ACCOUNT_SID"
export EM_TWILIO_AUTH_TOKEN="YOUR_TWILIO_ACCOUNT_AUTH_TOKEN"
export EM_TWILIO_NUMBER="YOUR_TWILIO_SENDER_NUMBER"
```
`NOTE: don't version control your set_env_vars file!`
- After filling out the correct values of the variables, run this to export them.
```bash
$ source set_env_vars
```

- Apply migrations and set up your initial database.

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py em_setup
```  

- Finally run the application using 

```bash
$ python manage.py runserver
```  

## File Structure

```bash
Entry_Management_App/
├── event_manager
│   ├── api
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── event_manager
│   │   ├── settings.py
│   │   └── urls.py
│   ├── management
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── mailing.py
│   │   ├── messaging.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── templates
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── media
│   │   └── static
│   ├── set_env_vars
│   ├── static
│   │   └── css
│   ├── templates
│   ├── users
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── managers.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── templates
│   │   ├── urls.py
│   │   └── views.py
│   └── visit
│       ├── admin.py
│       ├── forms.py
│       ├── migrations
│       ├── models.py
│       ├── serializers.py
│       └── views.py
├── LICENSE
├── README.md
└── requirements.txt
```


## Gallery

<p align="center">
  <img src="./gallery/img1.png">
</p>


## Credit/Acknowledgment
[![Contributors](https://img.shields.io/github/contributors/Vibhu-Agarwal/Entry_Management_App?style=for-the-badge)](https://github.com/Vibhu-Agarwal/Entry_Management_App/graphs/contributors)

## License
[![License](https://img.shields.io/github/license/Vibhu-Agarwal/Entry_Management_App?style=for-the-badge)](https://github.com/Vibhu-Agarwal/Entry_Management_App/blob/master/LICENSE)
