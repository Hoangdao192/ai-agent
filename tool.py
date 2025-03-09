import requests
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output
from typing import Any, Optional
from pydantic import BaseModel, Field


class GetWeather(BaseModel, Runnable):
    """Get the weather of a location using the Open-Meteo API"""

    id: str = Field(description="The ID of the tool")
    latitude: float = Field(description="Latitude of the location")
    longitude: float = Field(description="Longitude of the location")


    def invoke(
            self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any
        ) -> Output:
        print(f"Getting weather for {{{self.latitude}, {self.longitude}}}")
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        return response.json()["current"]