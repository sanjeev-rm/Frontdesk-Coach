#!/usr/bin/env python3
"""
Test script to debug Cornell API connection
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_api_connection():
    """Test the API connection and list available models"""

    print("Testing Cornell API connection...")
    print(f"API URL: {os.getenv('LLM_API_URL')}")
    print(f"API Key: {os.getenv('LLM_API_KEY')[:10]}...")

    try:
        # Initialize client
        client = OpenAI(
            api_key=os.getenv('LLM_API_KEY'),
            base_url=os.getenv('LLM_API_URL')
        )

        # Try to list models
        print("\nFetching available models...")
        models = client.models.list()

        print("Available models:")
        for model in models.data:
            print(f"  - {model.id}")

        # Try a simple completion
        print("\nTesting chat completion with openai.gpt-4o...")
        try:
            # Try v1.x API first
            response = client.chat.completions.create(
                model="openai.gpt-4o",
                messages=[{"role": "user", "content": "Hello, test message"}],
                max_tokens=50
            )
            print("v1.x API Success! Response:")
            print(response.choices[0].message.content)
        except Exception as v1_error:
            print(f"v1.x API failed: {v1_error}")
            try:
                # Try v0.x API
                response = client.ChatCompletion.create(
                    model="openai.gpt-4o",
                    messages=[{"role": "user", "content": "Hello, test message"}],
                    max_tokens=50
                )
                print("v0.x API Success! Response:")
                print(response.choices[0].message.content)
            except Exception as v0_error:
                print(f"v0.x API also failed: {v0_error}")

        # Test with system prompt like the application uses
        print("\nTesting with system prompt (like guest agent)...")
        system_prompt = """
        You are playing the role of a hotel guest who has encountered an issue and needs assistance from the front desk.
        Your goal is to create a realistic training scenario for front desk staff.
        Keep responses conversational and realistic.
        """

        user_message = """
        Based on this conversation:
        Guest: I have a problem with my room
        Agent: How can I help you?

        The front desk agent just said: "I'd be happy to help. What seems to be the issue?"

        How should the hotel guest respond? Consider realistic guest behavior.
        Generate a realistic guest response.
        """

        try:
            response = client.chat.completions.create(
                model="openai.gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            response_text = response.choices[0].message.content.strip()
            print(f"Complex message test Success! Response length: {len(response_text)}")
            print(f"Response preview: '{response_text[:200]}...'")
            print(f"Validation would pass: {len(response_text.strip()) > 0 and len(response_text) < 2000}")
        except Exception as e:
            print(f"Complex message test failed: {e}")

        # Test coach agent style message
        print("\nTesting coach agent style message...")
        coach_system = """
        You are an expert hotel service trainer providing real-time coaching to front desk agents.
        Your role is to help agents improve their customer service skills based on established training materials.
        Be constructive and supportive, never harsh or critical.
        """

        coach_user = """
        SITUATION: Guest is complaining about room cleanliness

        AGENT RESPONSE TO EVALUATE: "I'm sorry to hear that. Let me check with housekeeping."

        RELEVANT TRAINING CONTENT:
        - Maintain professional appearance
        - Demonstrate product knowledge
        - Show genuine care and concern

        CONVERSATION CONTEXT:
        Guest: My room wasn't cleaned properly
        Agent: I'm sorry to hear that. Let me check with housekeeping.

        Provide coaching feedback for this front desk agent response.
        """

        try:
            response = client.chat.completions.create(
                model="openai.gpt-4o",
                messages=[
                    {"role": "system", "content": coach_system},
                    {"role": "user", "content": coach_user}
                ],
                max_tokens=1500,
                temperature=0.9
            )
            response_text = response.choices[0].message.content.strip()
            print(f"Coach message test Success! Response length: {len(response_text)}")
            print(f"Response preview: '{response_text[:200]}...'")
            print(f"Validation would pass: {len(response_text.strip()) > 0 and len(response_text) < 2000}")
        except Exception as e:
            print(f"Coach message test failed: {e}")

    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_api_connection()