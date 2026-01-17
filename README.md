# BinDays Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![BinDays](https://img.shields.io/badge/Powered%20by-BinDays-blue)](https://bindays.app)

This custom component integrates **[BinDays](https://bindays.app)** into Home Assistant, allowing you to track your bin collection schedules.

## Features

*   **Next Collection Sensor:** Shows the date of the next bin collection.
*   **Attributes:** Provides details on which bins (and their colours) are being collected.
*   **Config Flow:** Easy setup via the Home Assistant UI (Postcode search -> Address selection).
*   **Robust Handling:** Supports complex council website interactions via the BinDays API.

## Installation

### Method 1: HACS (Recommended)

This integration is not yet in the default HACS repository, so you need to add it as a Custom Repository.

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

    <!-- [Screenshot: HACS Custom Repository Dialog] -->

3.  **Download:**
    *   The "BinDays" integration should now appear or be searchable.
    *   Click **Download**.
    *   Restart Home Assistant.

### Method 2: Manual Installation

1.  Download the latest release or clone this repository.
2.  Copy the `custom_components/bindays` folder to your Home Assistant `config/custom_components/` directory.
3.  Restart Home Assistant.

## Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** in the bottom right.
3.  Search for **BinDays**.

    <!-- [Screenshot: Add Integration Search] -->

4.  **Step 1:** Enter your **Postcode**.

    <!-- [Screenshot: Postcode Entry] -->

5.  **Step 2:** Select your **Address** from the list.

    <!-- [Screenshot: Address Selection] -->

6.  The integration will create a sensor (e.g., `sensor.next_collection`).

## Usage

The primary entity is `sensor.next_collection` (or similar, based on your address).

**State:** The date of the next collection (YYYY-MM-DD).

**Attributes:**
*   `bins`: List of bin names (e.g., `["General Waste", "Recycling"]`).
*   `colours`: List of bin colours (e.g., `["Black", "Green"]`).
*   `raw_bins`: Detailed list of dictionaries.

### Example Dashboard Card

```yaml
type: markdown
content: >
  **Next Collection:** {{ states('sensor.next_collection') }}
  
  **Bins:**
  {% for bin in state_attr('sensor.next_collection', 'bins') %}
  - {{ bin }}
  {% endfor %}
```
