from typing import Literal

from fastapi import HTTPException, Query

from app.utils.dataset_query import query_dataset
from app.utils.forest_dataset import DEFAULT_DATASET_PATH

from . import router


@router.get("/dataset/query")
def dataset_query(
    area: str | None = Query(default=None, description="Area filter matched against locality, stateProvince, or countryCode."),
    area_field: Literal["any", "locality", "stateProvince", "countryCode"] = Query(default="any"),
    species: str | None = Query(default=None, description="Species name or partial species name."),
    locality: str | None = Query(default=None, description="Locality substring match."),
    state_province: str | None = Query(default=None, alias="stateProvince", description="State or province substring match."),
    country_code: str | None = Query(default=None, alias="countryCode", description="Country code substring match."),
    min_individual_count: int | None = Query(default=None, ge=1),
    limit: int | None = Query(default=None, ge=1),
):
    try:
        analysis = query_dataset(
            DEFAULT_DATASET_PATH,
            area=area,
            area_field=area_field,
            species=species,
            locality=locality,
            state_province=state_province,
            country_code=country_code,
            min_individual_count=min_individual_count,
            limit=limit,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not query workbook: {exc}") from exc

    return {
        "status": "success",
        "dataset": DEFAULT_DATASET_PATH.name,
        "filters": {
            "area": area,
            "area_field": area_field,
            "species": species,
            "locality": locality,
            "stateProvince": state_province,
            "countryCode": country_code,
            "min_individual_count": min_individual_count,
            "limit": limit,
        },
        "records_read": analysis["records_read"],
        "records_matched": analysis["records_matched"],
        "records_returned": analysis["records_returned"],
        "summary": analysis["summary"],
        "results": analysis["results"],
    }