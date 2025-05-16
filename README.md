# berth planning

## api

- `GET /berth` - static berth data (structure of the port)

<details>
<summary>berth data json schema</summary>

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title":   "Berth Data",

  "type": "array",
  "items": {
    "type":    "object",
    "required": ["berthId", "dimensions", "limits", "equipment"],
    "properties": {
      "berthId": { "type": "string" },
      "dimensions": {
        "type": "object",
        "required": ["length_m", "width_m", "depth_m"],
        "properties": {
          "length_m": { "type": "number", "minimum": 1 },
          "width_m":  { "type": "number", "minimum": 1 },
          "depth_m":  { "type": "number", "minimum": 1 }
        }
      },
      "limits": {
        "type": "object",
        "required": ["maxLOA_m", "maxDraft_m"],
        "properties": {
          "maxLOA_m":    { "type": "number", "minimum": 1 },
          "maxBeam_m":   { "type": "number", "minimum": 1 },
          "maxDraft_m":  { "type": "number", "minimum": 1 },
          "maxDWT_t":    { "type": "number", "minimum": 1 },
          "allowedTypes": {
            "type": "array",
            "items": { "type": "string", "enum": ["CONTAINER", "RORO", "BULK", "TANKER", "CRUISE", "OTHER"] },
            "uniqueItems": true
          }
        }
      },
      "equipment": {
        "type": "object",
        "properties": {
          "gantryCranes":   { "type": "integer", "minimum": 0 },
          "mobileCranes":   { "type": "integer", "minimum": 0 },
          "roRoRamp":       { "type": "boolean" },
          "shorePower":     { "type": "boolean" }
        },
        "additionalProperties": false
      },
      "lastMaintenance": {
        "type": "string",
        "format": "date"
      }
    }
  }
}
```TANKERTANKER

</details>

- `GET /vessel/{id}`, `GET /vessel` - get the id/current vessel data. changes with additional actual data

<details>
<summary>vessel data json schema</summary>

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Vessel Data",
  "type": "array",
  "items": {
    "type": "object",
      "required": ["id", "imo", "name", "type", "loa_m", "beam_m", "draft_m", "eta"],
      "properties": {
        "id":       { "type": "string" },
        "imo":      { "type": "integer", "minimum": 1000000, "maximum": 9999999 },
        "name":     { "type": "string",  "maxLength": 64 },
        "type":     { "type": "string",  "enum": ["CONTAINER", "RORO", "BULK", "TANKER", "CRUISE", "OTHER"] },
        "loa_m":    { "type": "number",  "minimum": 0 },
        "beam_m":   { "type": "number",  "minimum": 0 },
        "draft_m":  { "type": "number",  "minimum": 0 },
        "eta":      { "type": "string",  "format": "date-time" }
    }
  }
}
```

</details>

- `PATCH /vessel` - provide actual data to the system. this changes `/vessel` endpoint

<details>
<summary>vessel data json schema</summary>

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Vessel Data",
  "type": "array",
  "items": {
    "type": "object",
      "required": ["id"],
      "properties": {
        "id":       { "type": "string" },
        "imo":      { "type": "integer", "minimum": 1000000, "maximum": 9999999 },
        "type":     { "type": "string",  "enum": ["CONTAINER", "RORO", "BULK", "TANKER", "CRUISE", "OTHER"] },
        "loa_m":    { "type": "number",  "minimum": 0 },
        "beam_m":   { "type": "number",  "minimum": 0 },
        "draft_m":  { "type": "number",  "minimum": 0 },
        "eta":      { "type": "string",  "format": "date-time" }
    }
  }
}
```

</details>

- `GET /plan/{vessel_id}` - berth plan recommended by the ml model for the vessels with id

<details>
<summary>berth plan data json schema</summary>

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Berth Plan Data",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["vesselId", "berthId", "start", "end"],
    "properties": {
      "properties": {
      "vesselId": { "type": "string" },
      "berthId":  { "type": "string" },
      "start":    { "type": "string", "format": "date-time" },
      "end":      { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

</details>

- `POST /fix` - human data from which the ml model learns
