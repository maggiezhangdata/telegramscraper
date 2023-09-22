import asyncio
import pandas as pd
import pickle
import json
from telethon import TelegramClient
from telethon.sessions import StringSession

# Function to get session string
async def get_session_string(api_id, api_hash, phone):
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input('Enter the OTP code sent to your phone: ')
            await client.sign_in(phone, code)
        session_string = client.session.save()
    return session_string

# Function to collect channel messages
# Function to collect channel messages
async def collect_channel_messages(api_id, api_hash, phone_number, channel_username, session_string=None, message_count=None):
    if session_string is None:
        session_string = await get_session_string(api_id, api_hash, phone_number)

    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        if not await client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code sent to your phone: '))
        
        channel_entity = await client.get_entity(channel_username)
        all_messages = []
        offset_id = 0
        collected = 0

        while True:
            # Check if we've collected enough messages
            if message_count is not None and collected >= message_count:
                break

            # Calculate the limit for the next query
            remaining = message_count - collected if message_count is not None else None
            limit = min(100, remaining) if remaining is not None else 100

            history = await client.get_messages(channel_entity, limit=limit, offset_id=offset_id)
            if not history:
                break

            all_messages.extend(history)
            offset_id = history[-1].id
            collected += len(history)
            print(f"Collected {collected} messages so far from channel: {channel_username}")

        # Truncate the list to the exact message count if necessary
        if message_count is not None:
            all_messages = all_messages[:message_count]

        # Convert messages to dictionaries
        message_data = [msg.to_dict() for msg in all_messages]
        
        print(f"Collections completed. Collected {len(message_data)} messages from channel: {channel_username}.")
        
        return message_data  # return list of message dictionaries


# Function to save data to a pickle file
def save_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Function to save data to a csv file
def save_to_csv(data, filename):
    df = pd.json_normalize(data)
    df.to_csv(filename, index=False)

# Function to save data to a json file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


# Example usage
# if __name__ == '__main__':
#     async def main():
#         api_id = 'your_api_id_here'
#         api_hash = 'your_api_hash_here'
#         phone_number = 'your_phone_number_here'
#         channel_username = 'some_channel_username_here'

#         df = await collect_channel_messages(api_id, api_hash, phone_number, channel_username)
#         print("Collection completed.")
#         print(df)
#         save_to_pickle(df, 'some_file.pkl')

#     asyncio.run(main())
