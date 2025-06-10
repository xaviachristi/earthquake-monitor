# Minimum Viable Product

- This document details the minimum viable product for the earthquake monitoring project

## Solution Contents
- Pipeline from API to cloud hosted storage
- Dashboard that integrates with storage
- Alert system
- Report generation
- Sibscription service

## Solution Characteristics
- Solution hosted in the cloud

## Pipeline
- Extract, transform and load module
- Load module must output data that can be used by notifications service
- Pipeline script
- Containerised
- Ran on continous schedule

## API
- API for querying historical earthquake data
- Can filter by region
- Can filter by time
- Constant uptime

## Dashboard
- Dashboard for monitoring historical earthquake data
- Can filter by region
- Can filter by time
- Has a page for reports
- Has a page for the API documentation
- Has a subscription form
- Constant uptime

## Reports
- PDF reports generated for earthquake activity
- PDF reports stored for reference
- Displayed in Dashboard

## Subscriptions
- Subscription service for receiving alerts and reports
- Needs multiple topics in AWS
- One topic per interest area (magnitude, location)
- Information stored in database

## Notifications
- Email alerts based on earthquake activity
- Only goes to subscribed individuals
- Lambderised
- Triggered by state machine and output of pipeline lambda
