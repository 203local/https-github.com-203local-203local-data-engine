# 203local Data Engine v1.0 - Generic Merge Manager

This adds a generic merge manager that can merge approved enrichment results into the master workbook.

## What it does

- Reads the latest `*_results.csv` from `enrichment/results/`
- Only processes rows where `ready_to_merge = Yes`
- Matches records using `business_id`
- Updates blank fields only by default
- Creates a backup before saving
- Uses Safe Save
- Creates a merge report
- Logs the merge in `logs/change_log.xlsx`

## Current supported mappings

- `suggested_website` -> `website`
- `suggested_email` -> `email`
- `suggested_phone` -> `phone`
- `suggested_instagram` -> `instagram`
- `suggested_facebook` -> `facebook`
- `suggested_tiktok` -> `tiktok`
- `suggested_linkedin` -> `linkedin`
- `suggested_youtube` -> `youtube`
- `suggested_menu_link` -> `menu_link`
- `suggested_reservation_link` -> `reservation_link`
- `suggested_reservation_platform` -> `reservation_platform`
- `suggested_delivery_platforms` -> `delivery_platforms`

## Run

From the project folder:

```bash
python3 scripts/generic_merge_manager.py
```
