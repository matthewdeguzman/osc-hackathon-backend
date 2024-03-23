from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
import models

app = FastAPI()
