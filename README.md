# BinDays Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![BinDays](https://img.shields.io/badge/Powered%20by-BinDays-blue)](https://bindays.app)

This custom component integrates **[BinDays](https://bindays.app)** into Home Assistant, allowing you to track your bin collection schedules directly from your dashboard.

## Features

*   **Next Collection Sensor:** Shows the date of the upcoming bin collection.
*   **Detailed Attributes:** Provides specific bin names, their colours, and raw collection data.
*   **Smart Config Flow:** Simple setup via the Home Assistant UI with automatic council detection and confirmation.
*   **Manual Override:** Option to manually select your council if the automatic matching is incorrect.
*   **Alphabetical Sorting:** Easy address selection from a sorted property list.
*   **Robust Error Guidance:** Helpful instructions and links if your postcode or council is not yet supported.

## Installation

### Method 1: HACS (Recommended)

1.  **Install HACS:**
    If you haven't already, install HACS by following the official instructions:
    [Download HACS](https://www.hacs.xyz/docs/use/download/download/)

2.  **Add Custom Repository:**
    *   Go to HACS in the sidebar.
    *   Click on **Integrations**.
    *   Click the 3 dots in the top right corner and select **Custom repositories**.
    *   **Repository:** `https://github.com/BadgerHobbs/BinDays-HomeAssistant`
    *   **Category:** `Integration`
    *   Click **Add**.

3.  **Download:**
    *   Search for "BinDays" and click **Download**.
    *   Restart Home Assistant.

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

The primary entity is `sensor.next_collection` (or similar, based on your address).

**State:** The date of the next collection (YYYY-MM-DD).

**Attributes:**
*   `bins`: List of bin names (e.g. `["General Waste", "Recycling"]`).
*   `colours`: List of bin colours (e.g. `["Black", "Green"]`).
*   `raw_bins`: Detailed list of dictionaries.

### Data Refresh
The integration automatically refreshes your bin collection data every **12 hours**.

### Example Dashboard Card

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

## Troubleshooting

If you encounter issues during setup or data retrieval:

*   **Unsupported Council**: If your council is not yet supported, please request support by opening an issue at [BinDays-API Issues](https://github.com/BadgerHobbs/BinDays-API/issues).
*   **Incorrect Address Data**: Report specific council or address lookup issues at [BinDays-API Issues](https://github.com/BadgerHobbs/BinDays-API/issues).
*   **Integration Crashes**: For issues specific to the Home Assistant integration (connection failures, sensor errors), please report them at [BinDays-HomeAssistant Issues](https://github.com/BadgerHobbs/BinDays-HomeAssistant/issues).