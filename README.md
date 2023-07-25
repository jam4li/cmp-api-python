# CMP Web Services

## Table of Contents

- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Installation](#installation)


## Project Directory Structure
```bash
.
├── Dockerfile
├── README.md
├── apps
│   ├── __init__.py
│   ├── backup
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── banner
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── base
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── signals.py
│   ├── exchange
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── invest
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── network
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   ├── utils
│   │   │   └── transfer.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── package
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   ├── utils.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── payment
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── test_models.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── purchase
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── support
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── telegram
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── cancel.py
│   │   │   ├── company.py
│   │   │   ├── educate.py
│   │   │   ├── home.py
│   │   │   ├── main.py
│   │   │   ├── settings.py
│   │   │   ├── start.py
│   │   │   └── support.py
│   │   └── views.py
│   ├── transaction
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   └── test_user_views.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── trc20
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_user_serializers.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   ├── utils
│   │   │   └── coinremitter.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── users
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   ├── utils
│   │   │   ├── google_auth.py
│   │   │   └── register.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   ├── wallet
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_serializers.py
│   │   ├── urls
│   │   │   ├── __init__.py
│   │   │   └── user_urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_views.py
│   └── withdraw
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers
│       │   ├── __init__.py
│       │   └── user_serializers.py
│       ├── urls
│       │   ├── __init__.py
│       │   └── user_urls.py
│       └── views
│           ├── __init__.py
│           └── user_views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── staging.py
│   ├── urls.py
│   └── wsgi.py
├── data
│   ├── certs
│   └── nginx
│       ├── nginx.dev.conf
│       ├── nginx.prod.conf
│       └── nginx.staging.conf
├── docker-compose.dev.yaml
├── docker-compose.prod.yaml
├── docker-compose.staging.yaml
├── entrypoint.sh
├── .env
├── .env.example
├── .gitignore
├── google-auth.json
├── locale
│   └── fa
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── logs
│   └── django.log
├── manage.py
├── remove.sh
├── requirements.txt
├── templates
│   └── updaing.html
└── utils
    ├── __init__.py
    ├── backup.py
    ├── calculate_binary_place.py
    ├── calculate_count.py
    ├── calculate_holidays.py
    ├── calculate_invest.py
    ├── calculate_invest_parent_binary_amount.py
    ├── calculate_last_invest.py
    ├── calculate_network.py
    ├── calculate_relation.py
    ├── calculate_status.py
    ├── calculate_total_amount.py
    ├── calculate_total_invest.py
    ├── db_migration
    │   ├── announcement.py
    │   ├── banner.py
    │   ├── cmp_claim_history.py
    │   ├── config.py
    │   ├── daily_profit.py
    │   ├── invest.py
    │   ├── network.py
    │   ├── network_transaction.py
    │   ├── package.py
    │   ├── payment.py
    │   ├── referral.py
    │   ├── transaction.py
    │   ├── users.py
    │   ├── wallet.py
    │   └── withdraw.py
    ├── django_migration
    │   ├── banner_banner.py
    │   ├── exchange_exchangeparent.py
    │   ├── invest_invest.py
    │   ├── network_network.py
    │   ├── package_package.py
    │   ├── referral_referral.py
    │   ├── support_supportdepartment.py
    │   ├── support_supportticket.py
    │   ├── users_user.py
    │   ├── users_userprofile.py
    │   ├── wallet_wallet.py
    │   └── withdraw_withdraw.py
    ├── exception_handler.py
    ├── find_binary_parent.py
    ├── response.py
    ├── tasks
    │   ├── __init__.py
    │   └── daily_profit.py
    └── transfer2.py
```

## Configuration
Before running the project, make sure to set these environment variables either in a `.env` file (for local development) or through your server's environment configuration. Properly configuring these variables will ensure the smooth functioning of your project.

#### Django Project Configuration
- **SECRET_KEY**: The Django project's secret key used for cryptographic signing. Keep this key confidential and do not share it publicly.
- **LOGLEVEL**: The logging level for the Django project. It determines the severity of logs to be recorded (e.g., DEBUG, INFO, WARNING, ERROR, etc.).

#### Database Variables

- **DATABASE**: The database (e.g., MySql, PostgreSql).
- **DATABASE_NAME**: The name of the database.
- **DATABASE_USERNAME**: The username to access the database.
- **DATABASE_PASSWORD**: The password for the database user.
- **DATABASE_HOST**: The host address of the database server.
- **DATABASE_PORT**: The port number for the database server.

#### Tether Payment Gateway Variables
- **TETHER_FIRST_API_KEY**:
- **TETHER_SECOND_API_KEY**:
- **TETHER_GATEWAY_URL**:
- **TETHER_NOTIFY_URL**:
- **TETHER_EXPIRE_TIME**:
- **TETHER_PASSWORD**:

#### Celery Variables
- **CELERY_BROKER_URL**: The URL for the Celery message broker (e.g., RabbitMQ, Redis).
- **CELERY_RESULT_BACKEND**: The result backend for Celery (e.g., RabbitMQ, Redis).

#### Telegram Bot Token
- **TELEGRAM_BOT_TOKEN**: The token provided by the Telegram Bot API to interact with your Telegram bot.

#### AWS Configuration
- **AWS_ENDPOINT_URL**: The AWS url for API requests.
- **AWS_ACCESS_KEY**: The AWS access key for authenticating API requests.
- **AWS_SECRET_KEY**: The AWS secret key for authenticating API requests.

## Installation
To set up the Project, follow these steps:

1. **Install Docker and Docker Compose:** If you don't have Docker and Docker Compose installed, follow the instructions for your operating system:
    - [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)
    - [Docker Desktop for macOS](https://docs.docker.com/desktop/mac/install/)
    - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. **Clone the repository:**
    ```bash
    git clone https://github.com/jam4li/cmp-api-python.git
    cd cmp-api-python
    ```

3. **Create the necessary configuration files:**
    * Add the google-auth.json file with the necessary OAuth 2.0 data to the project root.

4. **Choose the appropriate Docker Compose file for your environment:**
    * For development, use docker-compose.dev.yaml:
        ```bash
        docker-compose -f docker-compose.dev.yaml build
        docker-compose -f docker-compose.dev.yaml up -d
        ```

    * For staging, use docker-compose.staging.yaml:
        ```bash
        docker-compose -f docker-compose.staging.yaml build
        docker-compose -f docker-compose.staging.yaml up -d
        ```

    * For production, use docker-compose.prod.yaml:
        ```bash
        docker-compose -f docker-compose.prod.yaml build
        docker-compose -f docker-compose.prod.yaml up -d
        ```