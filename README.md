# telegram_scraper

`telegram_scraper` is a Python package designed to simplify the scraping of public information from Telegram groups and channels. It is built on top of the Telegram API and aims to make data collection easy and efficient.

## Prerequisites

Before you can use this package, you need to obtain an API ID and API hash from Telegram. Follow these steps to do so:

1. **Sign Up**: Create an account on Telegram using any of the Telegram applications.
2. **Login**: Log into your Telegram core account by visiting [Telegram Core](https://my.telegram.org).
3. **API Tools**: Navigate to the "API development tools" section and fill out the form.
4. **Credentials**: After submitting the form, you'll receive your <b>`api_id`</b> and <b>`api_hash`</b>, which are required for user authentication in the package.

## Installation

To install the development version of `telegram_scraper`, execute the following command:

```bash
pip install git+https://github.com/maggiezhangdata/telegram_scraper.git
```

Also, remember to install all required dependencies:

```bash
pip install -r requirements.txt
```

# Usage
## Importing the Package and Setting Up
First, import the package and initialize your API credentials:

```python
from telegram_scraper import collect_channel_messages
import asyncio
```
## Collect All Messages
To collect all messages from a specific Telegram channel, you can run:

```python
loop = asyncio.get_event_loop()
data = loop.run_until_complete(collect_channel_messages(api_id, api_hash, phone_number, channel_username))
```
## Collect a Subset of Messages
To collect only the latest 200 messages, for example, use:

```python
loop = asyncio.get_event_loop()
data = loop.run_until_complete(collect_channel_messages(api_id, api_hash, phone_number, channel_username, message_count=200))
```
This returns a list of dictionaries, each containing information about individual messages, represented with keys such as 'id', 'date', 'message', and so forth.

# Saving Data
You can save the collected data in various formats like CSV, JSON, or Pickle:

```python
from telegram_scraper import save_to_csv, save_to_json, save_to_pickle

save_to_csv(data, 'data.csv')
save_to_json(data, 'data.json')
save_to_pickle(data, 'data.pkl')
```