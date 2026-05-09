import importlib

# Provider registry: Maps provider names to their module and class paths
# This allows for lazy loading of providers only when needed.
PROVIDER_REGISTRY = {
    "gemini": ("termai.providers.gemini", "GeminiProvider"),
    "openai": ("termai.providers.openai", "OpenAIProvider"),
}

_provider_instances = {}

def get_provider(name):
    """
    Lazily loads and returns a provider instance.
    """
    if name in _provider_instances:
        return _provider_instances[name]

    if name not in PROVIDER_REGISTRY:
        return None

    module_path, class_name = PROVIDER_REGISTRY[name]
    try:
        module = importlib.import_module(module_path)
        provider_class = getattr(module, class_name)
        instance = provider_class()
        _provider_instances[name] = instance
        return instance
    except (ImportError, AttributeError) as e:
        print(f"[Error] Failed to load provider '{name}': {e}")
        return None

def send_request(config, user_input, debug_mode):
    provider_name = config.get("provider", "gemini")
    provider = get_provider(provider_name)

    if not provider:
        print(f"[Error] Provider '{provider_name}' is not supported or failed to load.")
        return 1

    return provider.send_request(config, user_input, debug_mode)

# Keep these for backward compatibility if needed in other parts of the code
def send_gemini_request(config, user_input, debug_mode):
    return get_provider("gemini").send_request(config, user_input, debug_mode)

def send_openai_request(config, user_input, debug_mode):
    return get_provider("openai").send_request(config, user_input, debug_mode)
