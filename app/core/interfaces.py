from abc import ABC, abstractmethod
from typing import Optional

class ImageGenerator(ABC):
    """
    Interface for image generation providers.
    Following the Interface Segregation and Liskov Substitution principles.
    """
    @abstractmethod
    def generate(self, prompt: str) -> Optional[bytes]:
        """
        Generates an image from a prompt and returns the raw bytes.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
