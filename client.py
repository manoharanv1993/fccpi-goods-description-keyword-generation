from typing import Literal

from langchain_openai import AzureChatOpenAI, AzureOpenAI, AzureOpenAIEmbeddings

API_BASE = "https://lnrsapim.azure-api.net/vnet"
DEFAULT_API_VERSION = "2023-05-15"
DEFAULT_MODEL = "gpt-35-turbo"
# DEFAULT_API_VERSION = "2023-05-15"
# DEFAULT_MODEL = "gpt-4"

class RiskAzureChatOpenAI(AzureChatOpenAI):
    """
    A class that represents the Risk Azure Chat OpenAI.

    Inherits from AzureChatOpenAI and provides additional functionality for preparing requests.

    Args:
        openai_api_key (str): The OpenAI API key.

    """
    deployment_name: Literal["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4", "gpt-4-32k"] = DEFAULT_MODEL
    openai_api_version: Literal["2022-12-01", "2023-03-15-preview", "2023-05-15", "2023-06-01-preview",
                                "2023-07-01-preview", "2023-08-01-preview", "2023-09-01-preview","2024-02-15-preview"] = DEFAULT_API_VERSION

    def __init__(self, deployment_name = DEFAULT_MODEL,
                 openai_api_version = DEFAULT_API_VERSION, *args, **kwargs):
        kwargs["validate_base_url"] = False
        kwargs["openai_api_base"] = API_BASE
        kwargs["model"] = deployment_name
        kwargs["openai_api_version"] = openai_api_version
        super().__init__(*args, **kwargs)
        self.client._client._prepare_request = self.prepare_request  # noqa: SLF001
        self.async_client._client._prepare_options = self.prepare_options  # noqa: SLF001

    def prepare_request(self, request):
        """
        Prepare the request by removing the "api-key" header. Otherwise, the request will fail with a 401.

        Args:
            request (Request): The request object.

        """
        request.headers["Ocp-Apim-Subscription-Key"] = request.headers["api-key"]
        del request.headers["api-key"]

    async def prepare_options(self, options) -> None:
        headers = {}
        options.headers = headers
        options.headers["Ocp-Apim-Subscription-Key"] = self.openai_api_key.get_secret_value()

        return await super(type(self.async_client._client), self.async_client._client)._prepare_options(options)  # noqa: SLF001

class RiskAzureOpenAI(AzureOpenAI):
    """
    A class representing RiskAzureOpenAI, which is a subclass of AzureOpenAI.
    It provides additional functionality for preparing requests and handling headers.

    Args:
        openai_api_key (str): The OpenAI API key.

    """

    def __init__(self, deployment_name = "text-davinci-003",
                 openai_api_version = DEFAULT_API_VERSION, *args, **kwargs):
        kwargs["validate_base_url"] = False
        kwargs["openai_api_base"] = API_BASE
        kwargs["deployment_name"] = deployment_name
        kwargs["openai_api_version"] = openai_api_version
        super().__init__(*args, **kwargs)
        self.client._client._prepare_request = self.prepare_request  # noqa: SLF001

    def prepare_request(self, request):
        """
        Prepare the request by removing the "api-key" header. Otherwise, the request will fail with a 401.

        Args:
            request (Request): The request object.

        """
        request.headers["Ocp-Apim-Subscription-Key"] = request.headers["api-key"]
        del request.headers["api-key"]

class RiskAzureOpenAIEmbeddings(AzureOpenAIEmbeddings):
    """
    A class representing RiskAzureOpenAIEmbeddings, which is a subclass of AzureOpenAIEmbeddings.
    It provides additional functionality for preparing requests and handling headers.

    Args:
        openai_api_key (str): The OpenAI API key.

    """

    def __init__(self, deployment_name = "text-embedding-ada-002",
                 openai_api_version = DEFAULT_API_VERSION, *args, **kwargs):
        kwargs["validate_base_url"] = False
        kwargs["openai_api_base"] = API_BASE
        kwargs["deployment"] = deployment_name
        kwargs["openai_api_version"] = openai_api_version
        super().__init__(*args, **kwargs)
        self.client._client._prepare_request = self.prepare_request  # noqa: SLF001
        self.async_client._client._prepare_options = self.prepare_options  # noqa: SLF001

    def prepare_request(self, request):
        """
        Prepare the request by removing the "api-key" header. Otherwise, the request will fail with a 401.

        Args:
            request (Request): The request object.

        """
        request.headers["Ocp-Apim-Subscription-Key"] = request.headers["api-key"]
        del request.headers["api-key"]

    async def prepare_options(self, options) -> None:
        headers = {}
        options.headers = headers
        options.headers["Ocp-Apim-Subscription-Key"] = self.openai_api_key.get_secret_value()

        return await super(type(self.async_client._client), self.async_client._client)._prepare_options(options)  # noqa: SLF001

if __name__ == "__main__":
    # export RISK_API_KEY=<your-risk-api-key> && poetry run python src/client.py "What is the capital of France?"
    import os
    import sys

    if len(sys.argv) > 1:
        question = sys.argv[1]

    api_key = os.getenv("RISK_API_KEY")
    llm = RiskAzureChatOpenAI(openai_api_key=api_key, temperature=0.)

    result = llm.invoke(question)
    print(result.content)