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

The repository includes the workbook `0009156-260519110011954.xlsx` in the project root, and the `/forest` endpoint uses it by default.

Example request:

```bash
POST /forest?area=Bagmati&area_field=stateProvince
```

You can also upload a replacement `.xlsx` file as `dataset` to analyze a different workbook with the same occurrence fields.
