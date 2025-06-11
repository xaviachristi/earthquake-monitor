# Minimum Viable Product

This document details the minimum viable product for the earthquake monitoring project.

## Solution Contents
- Pipeline from API, refreshed very minute, to cloud hosted historical storage
- Pipeline stores realtime data in historic storage
- Dashboard that integrates with storage
- Alert system
- Report generation
- Subscription service

## Solution Characteristics
- Solution hosted on the cloud

## Pipeline
- Extract, transform and load modules
- Load module must output data that can be used by the notifications service
- Pipeline script
- Containerised
- Ran on continous schedule every minute

## API
- API for querying historical earthquake data
- Can filter by region
- Can filter by time
- Can filter by magnitude
- Constant uptime

## Dashboard
- Dashboard for monitoring historical earthquake data
- Can filter by region
- Can filter by time
- Can filter by magnitude
- Has a page for reports
- Has a page for the API documentation
- Has a subscription form
- Constant uptime

## Reports
- PDF reports generated for earthquake activity
- PDF reports stored for reference
- Reports are generated once a day
- Displayed in Dashboard

## Subscriptions
- Subscription service for receiving alerts for earthquakes
- Needs multiple topics in AWS
- One topic per interest area (magnitude, location in name)
- Used to determine what email adresses recieve alerts from what topics
- Alerts are potentially triggered every minute

## Notifications
- Email alerts based on earthquake activity
- Only goes to subscribed individuals
- Lambderised
- Triggered by state machine and output of pipeline lambda
- Triggered at most once a minute
