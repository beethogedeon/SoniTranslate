from os.path import join

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from api.models import DubbingRequest

from soni_translate.logging_setup import (
    logger,
    set_logging_level,
    configure_logging_libs,
); configure_logging_libs()

from soni_translate.mdx_net import (
    UVR_MODELS,
    MDX_DOWNLOAD_LINK,
    mdxnet_models_dir,
)
from soni_translate.utils import download_manager, upload_model_list

from app_rvc import SoniTranslate


for id_model in UVR_MODELS:
    download_manager(
        join(MDX_DOWNLOAD_LINK, id_model), mdxnet_models_dir
    )

models_path, index_path = upload_model_list()

VideoDubber = SoniTranslate()


app = FastAPI(title="Video Dubbing", version="0.0.2")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/dubbing")
async def translate(data: DubbingRequest):
    result = await VideoDubber.multilingual_media_conversion(**data)
    return result