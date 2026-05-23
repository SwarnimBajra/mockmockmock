from typing import Literal

from fastapi import File, HTTPException, Query, UploadFile

from app.utils.forest_dataset import DEFAULT_DATASET_PATH, analyze_dataset

from . import router


@router.post("/forest")
async def forest(
    area: str | None = Query(default=None, description="Area filter matched against locality, stateProvince, or countryCode."),
    area_field: Literal["any", "locality", "stateProvince", "countryCode"] = Query(default="any"),
    dataset: UploadFile | None = File(default=None),
):
    try:
        if dataset is None:
            source = DEFAULT_DATASET_PATH
            dataset_name = source.name
        else:
            source = await dataset.read()
            dataset_name = dataset.filename or "uploaded.xlsx"

        analysis = analyze_dataset(source, area=area, area_field=area_field)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not analyze workbook: {exc}") from exc

    return {
        "status": "success",
        "dataset": dataset_name,
        "filters": {
            "area": area,
            "area_field": area_field,
        },
        "records_read": analysis["records_read"],
        "records_used": analysis["records_used"],
        "summary": analysis["summary"],
    }
