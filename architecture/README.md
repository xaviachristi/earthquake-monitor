# Architecture Overview

This directory contains the architecture and Entity-Relationship Diagram used for the Earthquake Monitoring System.


# Schema Details
- **earthquake**
  - Stores individual earthquake records with metadata like magnitude, time, location, and tsunami indicators.
- **state**
  - Maps U.S. states with associated metadata.
- **region**
  - Defines geographical regions (e.g., West Coast, Midwest).
- **state_region_interaction**
  - Join table that maps states to regions for querying.


## Files
- `architecture.png`: System-level AWS architecture.
- `erd.png`: Entity Relationship Diagram for the RDS database schema.

## Set-up Instructions
