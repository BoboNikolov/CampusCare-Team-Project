# CampusCare deployment checklist

## Before deployment

- Push the repository to GitHub.
- Confirm `render.yaml` is at the repository root.
- Confirm the final allowed NCI email domains with the lecturer or college account format.
- Remove any test or demo records that should not appear in the final presentation.

## Render Blueprint deployment

1. Sign in to Render.
2. Select **New > Blueprint**.
3. Connect the CampusCare GitHub repository.
4. Select the `main` branch.
5. Apply the Blueprint.
6. Wait for both `campuscare-db` and `campuscare-app` to become available.
7. Open `campuscare-app` and verify `/_stcore/health` returns a healthy response.

## Acceptance test after deployment

1. Register two different NCI-domain accounts.
2. Account A creates a donation.
3. Account B finds and reserves the donation.
4. Account A sees the receiver and completes the handover.
5. Both accounts show updated activity and trust scores.
6. Refresh the browser and confirm data remains stored in PostgreSQL.
7. Restart/redeploy the web service and confirm the records remain available.

## Required final-demo evidence

- Public deployed URL
- Successful login and registration
- Donation creation
- Search/filter flow
- Reservation and handover flow
- Profile and trust score
- Render PostgreSQL resource visible in the dashboard
- GitHub commit history and team contributions

## Current Render free-tier warning

Render free PostgreSQL databases expire 30 days after creation. Create the final demonstration database close enough to the presentation date, or move it to a paid database before expiry. Do not treat a free database as permanent storage.

The Blueprint uses `autoDeployTrigger: checksPass`, so automatic deployment waits for the GitHub test checks to pass.
