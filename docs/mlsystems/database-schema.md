# Database Schema

## Storage

MMAlytics uses PostgreSQL for persistent data storage.

## Purpose

The database stores historical MMA data used by the data pipeline,
feature engineering process, and predictive models.

## Design

The database separates persistent historical data from
model-specific transformations and feature generation.