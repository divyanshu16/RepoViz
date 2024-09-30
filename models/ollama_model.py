import requests
import json


class OllamaModel:
    def __init__(self, model_name, host='localhost', port=11434):
        """
        Initializes the OllamaModel class with the model name and the API host/port.

        Args:
            model_name (str): The name of the model to load.
            host (str): The host where the Ollama API is running (default: localhost).
            port (int): The port where the Ollama API is running (default: 11434).
        """
        self.model_name = model_name
        self.base_url = f"http://{host}:{port}/api/generate"
        self.headers = {
            'Content-Type': 'application/json',
            # Add more headers here if needed, e.g., authorization
        }

        print({
            "self.model_name": self.model_name,
            "self.base_url": self.base_url,
            "self.headers": self.headers
        })

    def generate(self, prompt, only_response_text=True):
        """
        Sends a prompt to the model and retrieves a response.

        Args:
            prompt (str): The input prompt to send to the model.

        Returns:
            dict: The JSON response from the API.
        """
        payload = {
            'model': self.model_name,
            'prompt': prompt,
            "stream": False
        }

        print(f"Hitting call at {self.base_url}\nwith headers: {self.headers}\ndata: {payload}\n\n\n\n")
        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))

            # Check if the request was successful
            if response.status_code == 200:
                if only_response_text:
                    return response.json()["response"]
                return response.json()
            else:
                response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None

    def set_headers(self, headers):
        """
        Allows updating the headers, for example, if you need to set authorization.

        Args:
            headers (dict): A dictionary containing headers to be set.
        """
        self.headers.update(headers)


# Example Usage
def example_usage():
    # Initialize the Ollama model with the model name
    OLLAMA_MODEL_ID = "codegemma:7b"
    model = OllamaModel(model_name=OLLAMA_MODEL_ID)

    # Send a prompt to the model
    response = model.generate(prompt="What is the capital of France?")

    # Check the response
    if response:
        print("Model Response:", response)
    else:
        print("Failed to get a response from the model.")


example_usage()
