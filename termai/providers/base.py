from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def send_request(self, config, user_input, debug_mode):
        """Send a request to the AI model."""
        pass
