# MockingBird

Run

```
uv run uvicorn app:app --reload
```

**api testing**

```
http://127.0.0.1:8000/docs
```

## Forest analysis

Run `script/download.py` to fetch the workbook into `data/birds_dataset.xlsx`. The `/forest` endpoint and the new dataset query endpoint use that file by default, with the root-level workbook kept as a fallback for older clones.

Example request:

```bash
POST /forest?area=Bagmati&area_field=stateProvince
```

You can also upload a replacement `.xlsx` file as `dataset` to analyze a different workbook with the same occurrence fields.

## Dataset query

Use the query endpoint when you want filtered rows back from the workbook instead of the health summary.

Example request:

```bash
GET /dataset/query?species=bulbul&countryCode=NP&limit=10
```
