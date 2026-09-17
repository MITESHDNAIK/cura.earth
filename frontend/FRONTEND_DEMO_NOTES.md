# Cura.Earth Frontend — Demo Integration Notes

## What was changed

- Chat now uses the working multi-turn endpoint:
  `POST /api/v1/conversation/conversation`
- The frontend keeps a lightweight environmental profile from the user's conversation so the What-If simulator receives the same SOC, rainfall, crop and land-use context.
- Clarification quick-actions are translated into natural-language inputs that the backend extractor can understand.
- Chat → diagnosis → What-If is now one continuous flow.
- Added small status chips for multi-metric reasoning and scientific evidence.

## Run

From this `frontend` directory:

```powershell
npm install
npm run dev
```

The Vite proxy should forward `/api` requests to the FastAPI backend according to `vite.config.js`.

## Backend

Start the backend first:

```powershell
cd ..\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Then start the frontend in a second terminal.

## Recommended demo

1. Scientist tab: `Biodiversity is declining on my wheat farm.`
2. Add: `The soil organic carbon is 0.3%.`
3. Add: `Rainfall is low.`
4. Add: `I grow wheat and use monoculture.`
5. Open **What if?** on the recommendation.
6. Run **Agroforestry / tree-crop integration** for 5 years.
7. Point out the connected SOC, water retention, microbial diversity, pollinator richness and habitat-fragmentation trajectory.
8. Keep the simulator disclaimer visible: projections are illustrative, not site-specific forecasts.
