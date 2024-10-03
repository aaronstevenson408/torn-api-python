# TornAPI Wrapper

A Python wrapper for the Torn API, designed to simplify interactions with the Torn RPG game. This project provides an easy-to-use interface for accessing various features of the Torn API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#Configuration)
- [Usage](#usage)
- [Example Usage](#example-usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetch user data and selections.
- Rate limiting to manage API calls efficiently.
- Support for multiple sections (e.g., User,Property, etc)
- Built-in logging for debugging and tracking.

## Installation

To install the TornAPI wrapper, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/tornapi-wrapper.git
cd tornapi-wrapper
pip install -r requirements.txt
```
## Configuration

Create a `.env` file in the root directory of your project and add the following variables:

```plaintext
# .env

# Debug Level
DEBUG_LEVEL=Critical  # Change this to INFO, WARNING, ERROR, or CRITICAL as needed

# Test Variables
Test-Full=
Test-Limited=
Test-Min=
Test-Public=

## Usage

To use the TornAPI wrapper, initialize the API without needing to specify your Torn API key explicitly, and use the `Sections` class to access various user-related features. Here’s a simple example:

```python
from tornApi import TornAPI
from sections import Sections

api = TornAPI()  # Initializes the TornAPI instance
sections = Sections(api)  # Initializes the Sections class
```

You can then interact with the API to fetch user data as follows:

```python
user = sections.user('')  # Replace with a valid user ID
user_properties = user.properties.fetch_properties()
print(user_properties.properties[0].property_data)
```

## Example Usage

Here’s a concise example demonstrating various API calls:

```python
from tornApi import TornAPI
from sections import Sections

api = TornAPI()
sections = Sections(api)
user = sections.user('')  # Replace with a valid user ID

# Fetching user properties and displaying data
user_properties = user.properties.fetch_properties()
property = sections.property(user_properties.properties[0].id)

# Fetching various user data
print(user.basic.fetch_basic())
print(user.ammo.fetch_ammo())
print(user.skills.fetch_skills())
print(property.property.fetch_data())

api.close()
```

## API Reference

For detailed information on the available methods and classes, refer to the [Unofficial Torn API documentation](https://tornapi.tornplayground.eu/user/properties).

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```