# BinDays-HomeAssistant

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

![d2(14)](https://github.com/user-attachments/assets/02f11389-cc57-4a16-99d3-3209642e0d69)

<p align="center">
  <a href="https://github.com/BadgerHobbs/BinDays-App">BinDays-App</a> •
  <a href="https://github.com/BadgerHobbs/BinDays-Client">BinDays-Client</a> •
  <a href="https://github.com/BadgerHobbs/BinDays-API">BinDays-API</a> •
  <a href="https://github.com/BadgerHobbs/BinDays-HomeAssistant">BinDays-HomeAssistant</a>
</p>

> **Council-related issue?** For problems with a specific council's bin collection data or to request a new council, please open an issue in the [**BinDays-API repository**](https://github.com/BadgerHobbs/BinDays-API/issues).

## Overview

This is the repository for the BinDays Home Assistant integration, fetching your bin collection data from supported councils via the [BinDays-API](https://github.com/BadgerHobbs/BinDays-API).

## Features

- **Next Collection Sensor:** Shows the date of the upcoming bin collection.
- **Collection Schedule Sensor:** Provides a full list of all upcoming bin collection dates and their associated bins.
- **Detailed Attributes:** Provides specific bin names, their colours, and raw collection data.
- **Smart Config Flow:** Simple setup via the Home Assistant UI with automatic council detection and confirmation.
- **Manual Override:** Option to manually select your council if the automatic matching is incorrect.
- **Alphabetical Sorting:** Easy address selection from a sorted property list.
- **Robust Error Guidance:** Helpful instructions and links if your postcode or council is not yet supported.

## Installation

### Method 1: HACS (Recommended)

1.  **Install HACS:**
    If you haven't already, install HACS by following the official instructions:
    [Download HACS](https://www.hacs.xyz/docs/use/download/download/)

2.  **Add Custom Repository:**
    - Go to HACS in the sidebar.
    - Click on **Integrations**.
    - Click the 3 dots in the top right corner and select **Custom repositories**.
    - **Repository:** `https://github.com/BadgerHobbs/BinDays-HomeAssistant`
    - **Category:** `Integration`
    - Click **Add**.

3.  **Download:**
    - Search for "BinDays" and click **Download**.
    - Restart Home Assistant.

### Method 2: Manual Installation

1.  Download the latest release or clone this repository.
2.  Copy the `custom_components/bindays` folder to your Home Assistant `config/custom_components/` directory.
3.  Restart Home Assistant.

## Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** and search for **BinDays**.
3.  **Step 1:** Enter your **Postcode**.
4.  **Step 2:** **Confirm your Council**. The integration will automatically detect your local authority. If it's incorrect, you can select "No" to choose from a full list of supported councils.
5.  **Step 3:** Select your **Address** from the alphabetically sorted list.
6.  The integration will create a sensor (e.g. `sensor.next_collection`).

## Usage

The integration provides two main sensors:

### 1. Next Collection Sensor (`sensor.next_collection`)

**State:** The date of the next collection (YYYY-MM-DD).

**Attributes:**

- `bins`: List of bin names (e.g. `["General Waste", "Recycling"]`).
- `colours`: List of bin colours (e.g. `["Black", "Green"]`).
- `raw_bins`: Detailed list of dictionaries, including `name`, `colour`, `type`, and `keys`.

### 2. Collection Schedule Sensor (`sensor.collection_schedule`)

**State:** The number of upcoming collections currently in the schedule.

**Attributes:**

- `upcoming_collections`: A list of upcoming collection events. Each event contains:
  - `date`: The ISO formatted date of the collection.
  - `bins`: A list of bins for that date (with `name`, `colour`, `type`, and `keys`).

### Data Refresh

The integration automatically refreshes your bin collection data every **12 hours**.

### Example Dashboard Cards

#### Next Collection Summary

```yaml
type: markdown
content: >
  **Next Collection:** {{ states('sensor.next_collection') }}
  <br/>
  <br/>
  **Bins:**
  {% for raw_bin in state_attr('sensor.next_collection', 'raw_bins') %}
  <br/>- {{ raw_bin['name'] }} ({{ raw_bin['colour'] }})
  {% endfor %}
```

#### Full Collection Schedule

```yaml
type: markdown
content: >
  ### Upcoming Collections

  {% for event in state_attr('sensor.collection_schedule','upcoming_collections') %}
  <br/>
  **{{ as_timestamp(event.date) | timestamp_custom('%A, %d %b') }}**
  {% for bin in event.bins %}
  <br/>- {{ bin.name }} ({{ bin.colour }})
  {% endfor %}
  <br/>
  {% endfor %}
```

## Troubleshooting

If you encounter issues during setup or data retrieval:

- **Unsupported Council**: If your council is not yet supported, please request support by opening an issue at [BinDays-API Issues](https://github.com/BadgerHobbs/BinDays-API/issues).
- **Incorrect Address Data**: Report specific council or address lookup issues at [BinDays-API Issues](https://github.com/BadgerHobbs/BinDays-API/issues).
- **Integration Crashes**: For issues specific to the Home Assistant integration (connection failures, sensor errors), please report them at [BinDays-HomeAssistant Issues](https://github.com/BadgerHobbs/BinDays-HomeAssistant/issues).

## License

This project is licensed under the [GPLv3 License](LICENSE).

## Support

If you find this project helpful, please consider supporting its development.

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=badgerhobbs&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/badgerhobbs)

## Screenshots

### Postcode Input

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 15-21-04 Settings – Home Assistant" src="https://github.com/user-attachments/assets/148c7964-6a62-471d-8d13-9fb4e354a94c" />

### Collector Detection & Confirmation

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 15-21-18 Settings – Home Assistant" src="https://github.com/user-attachments/assets/db5cbe23-d5e4-4c61-8a1f-237e1ad63cd2" />

### Manual Collector Selection

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 15-21-28 Settings – Home Assistant" src="https://github.com/user-attachments/assets/004eef24-a6da-41fa-a781-4bc6db19f639" />

### Address Selection

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 15-21-37 Settings – Home Assistant" src="https://github.com/user-attachments/assets/b18b065e-a1df-4e4a-b48e-8eafbc66883c" />

### Configuration Creation

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 15-21-45 Settings – Home Assistant" src="https://github.com/user-attachments/assets/24ab7784-ed23-4204-ba2d-aa870217d9d6" />

### Multiple Address Support

<img width="1920" height="927" alt="image" src="https://github.com/user-attachments/assets/9069d0cc-a0a9-4c45-a71d-68dc4d8a5140" />

### Example Entity

<img width="1920" height="927" alt="image" src="https://github.com/user-attachments/assets/dd520dd4-ca84-4cd1-88bb-9cf34dd581d7" />

### Example Dashboard Cards

<img width="1920" height="927" alt="image" src="https://github.com/user-attachments/assets/b65070bd-9d1e-4e9e-934a-234de19356a0" />


