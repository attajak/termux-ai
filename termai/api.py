from .providers.gemini import GeminiProvider
from .providers.openai import OpenAIProvider

PROVIDERS = {
    "gemini": GeminiProvider(),
    "openai": OpenAIProvider()
}

def send_request(config, user_input, debug_mode):
    provider_name = config.get("provider", "gemini")
    provider = PROVIDERS.get(provider_name)

    if not provider:
        print(f"[Error] Provider '{provider_name}' is not supported.")
        return 1

    return provider.send_request(config, user_input, debug_mode)

# Keep these for backward compatibility if needed in other parts of the code
def send_gemini_request(config, user_input, debug_mode):
    return GeminiProvider().send_request(config, user_input, debug_mode)

def send_openai_request(config, user_input, debug_mode):
    return OpenAIProvider().send_request(config, user_input, debug_mode)
