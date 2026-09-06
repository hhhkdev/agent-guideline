# Architecture Guide

## 1. Directory Structure
```
src/
├── components/     # UI components
├── services/       # Business & API logic
└── utils/          # Helpers and shared utilities
```

## 2. 5-Layer Principles
- Keep modules loosely coupled.
- Encapsulate data fetching into dedicated service modules.
- Enforce strict type definitions across all domain models.
