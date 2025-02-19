
### GET `/profiles/profile/{profile_id}`

Publicly available. This endpoint returns a public profile by its unique identifier.

#### Response Example

```json
{
    "id": "368498e3-4254-4212-9319-228d0e589168",
    "public": true,
    "name": "admin",
    "total_skills": 2,
    "user": {
        "registration": 1739643143,
        "description": "🔥 Test Bio 🔥",
        "avatar_url": "https://www.gravatar.com/avatar/a2d6a7ecb918ece4f84f524b38969f75",
        "tags": [
            "TestModeActivated",
            "BreakingLimits",
            "NoRoomForErrors"
        ]
    },
    "root_skills": [
        {
            "skill": "mobile_app_developer",
            "skills": [
                {
                    "skill": "kotlin_native_app_developer",
                    "level": 9
                }
            ]
        },
        {
            "skill": "datenbank_experte",
            "skills": [
                {
                    "skill": "postgresql",
                    "level": 27
                }
            ]
        }
    ]
}
```

### PUT `/profiles/user/me/public-status`

The profile-status can be replaced by the users themselves or by an admin.

#### Request Example

```json
{
  "public": true
}
```

#### Response Example

```json
{
    "id": "368498e3-4254-4212-9319-228d0e589168",
    "public": false,
    "name": "admin",
    "total_skills": 2
}
```

### GET `/profiles/user/me/public-status`

Use user ID or the 'me' phrase to get profile status. If there is no profile, one will be initialized.

#### Response Example

```json
{
    "id": "368498e3-4254-4212-9319-228d0e589168",
    "public": false,
    "name": "admin",
    "total_skills": 2
}
```

## Development Setup

1. Install [Python 3.10](https://python.org/), [Poetry](https://python-poetry.org/) and [poethepoet](https://pypi.org/project/poethepoet/).
2. Clone this repository and `cd` into it.
3. Run `poe setup` to install the dependencies.
4. Run `poe api` to start the microservice. You can find the automatically generated swagger documentation on http://localhost:8001/docs.

## Poetry Scripts

```bash
poe setup           # setup dependencies, .env file and pre-commit hook
poe api             # start api locally
poe test            # run unit tests
poe pre-commit      # run pre-commit checks
  poe lint          # run linter
    poe format      # run auto formatter
      poe isort     # sort imports
      poe black     # reformat code
    poe ruff        # check code style
    poe mypy        # check typing
    poe flake8      # check code style
  poe coverage      # run unit tests with coverage
poe alembic         # use alembic to manage database migrations
poe migrate         # run database migrations
poe env             # show settings from .env file
poe jwt             # generate a jwt with the given payload and ttl in seconds
poe check           # check course definitions
poe sync_skills     # push local skills to backend (deprecated)
```

## PyCharm configuration

Configure the Python interpreter:

- Open PyCharm and go to `Settings` ➔ `Project` ➔ `Python Interpreter`
- Open the menu `Python Interpreter` and click on `Show All...`
- Click on the plus symbol
- Click on `Poetry Environment`
- Select `Existing environment` (setup the environment first by running `poe setup`)
- Confirm with `OK`

Setup the run configuration:

- Click on `Add Configuration...` ➔ `Add new...` ➔ `Python`
- Change target from `Script path` to `Module name` and choose the `api` module
- Change the working directory to root path ➔ `Edit Configurations` ➔ `Working directory`
- In the `EnvFile` tab add your `.env` file
- Confirm with `OK`