from typing import Optional
from mimetypes import MimeTypes
from google import genai
from google.genai.types import Part

__all__ = ["ApiCaller"]

MODEL_ID = 'gemini-2.0-flash-001'
LOCATION = 'us-central1'


class ApiCaller:
    def __init__(self, api_key: Optional[str] = None,) -> None:
        self._api_key = api_key
        self._genai_client = None
        
        if self._api_key is not None:
            self._genai_client = genai.Client(api_key=self._api_key)
        else:
            return "api_key not available"

    def extract(self, prompt_file: Optional[str],
                path: str) -> Optional[str]:
        prompt = self._get_prompt_part(prompt_file)
        file = self._get_file_part(path)

        response = self._genai_client.models.generate_content(  # type: ignore
            model=MODEL_ID, contents=[prompt, file]
        )

        return response.text

    def _get_file_part(self, path: str) -> Part:
        mime_type = MimeTypes().guess_type(path)[0] or \
            'application/octet-stream'

        with open(path, 'rb') as f:
            return Part.from_bytes(data=f.read(),
                                   mime_type=mime_type)

    def _get_prompt_part(self,
                         prompt_file: Optional[str]) -> Part:
        if (prompt_file is None):
            return "Either prompt_file must " + "be provided"
        else:
            with open(prompt_file, 'r') as f:
                prompt_text = f.read()

        return Part.from_text(text=prompt_text)  # type: ignore
