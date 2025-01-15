import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY", ""))

cache = {}


def get_openai_response(user_input: str):
    if user_input in cache:
        return cache[user_input]

    system_prompt = """
    You are a food ordering assistant that can process placing or canceling orders.
    Follow these rules:
    - For placing orders: Extract items and quantities, defaulting to 1 if unspecified.
    - For canceling orders: Extract and return the order ID.
    Provide all responses in JSON format as per the given schema.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "place_order",
                "description": "Extract the order item name and its quantity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of items to order with their quantities.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name of the item e.g., burger, fries, drink.",
                                        "enum": ["burger", "fries", "drink"],
                                    },
                                    "quantity": {
                                        "type": "string",
                                        "description": "Quantity of the item. e.g., 1, 2, 3.",
                                    },
                                },
                                "required": ["name", "quantity"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["items"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_order",
                "description": "Extracts the ID of the order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "The ID of the order to cancel.",
                        }
                    },
                    "required": ["id"],
                    "additionalProperties": False,
                },
            },
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant for processing orders.",
            },
            {"role": "user", "content": user_input},
        ],
        tools=tools,
    )

    cache[user_input] = response
    print(response)
    return response


# if __name__ == "__main__":
#     get_openai_response("I want to order fries for me and my friend")
