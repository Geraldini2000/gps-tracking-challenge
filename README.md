# GPS Tracking Backend

Backend responsible for receiving GPS data via TCP using a proprietary protocol
and exposing the latest device location through a REST API.

## Architecture Overview

- TCP Gateway (asyncio): receives and processes GPS messages
- Business rules with SOLID principles
- REST API (Django REST Framework) for querying device locations

## Project Structure

- tcp_gateway/: TCP ingestion layer
- api/: REST API
- shared/: shared contracts and utilities

## Status

Project under development
