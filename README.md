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

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 03-42-46 HACS – Home Assistant" src="https://github.com/user-attachments/assets/d07bf8e0-fc20-4728-8894-04dd346be7ad" />

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

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 03-44-30 Settings – Home Assistant" src="https://github.com/user-attachments/assets/f5cac10d-8ed7-431e-86d1-4a6936483bc2" />

4.  **Step 1:** Enter your **Postcode**.

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 05-28-28 Settings – Home Assistant" src="https://github.com/user-attachments/assets/6ed61d8d-5a24-43e4-b837-a0feac27e26e" />

5.  **Step 2:** Select your **Address** from the list.

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 05-28-37 Settings – Home Assistant" src="https://github.com/user-attachments/assets/374190ce-ee3b-493b-8576-5051abdada4f" />

6.  The integration will create a sensor (e.g. `sensor.next_collection`).

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 05-28-43 Settings – Home Assistant" src="https://github.com/user-attachments/assets/2fa6e331-7e08-4973-b4ee-00303c0f0879" />

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 05-28-57 Settings – Home Assistant" src="https://github.com/user-attachments/assets/44896752-3b4a-4bae-b402-9921b6f72613" />

<img width="1920" height="927" alt="Screenshot 2026-01-17 at 05-28-50 Settings – Home Assistant" src="https://github.com/user-attachments/assets/e8c07ca0-b7e4-4089-a3fc-9e43be323ee4" />

## Usage

The primary entity is `sensor.next_collection` (or similar, based on your address).

**State:** The date of the next collection (YYYY-MM-DD).

**Attributes:**
*   `bins`: List of bin names (e.g. `["General Waste", "Recycling"]`).
*   `colours`: List of bin colours (e.g. `["Black", "Green"]`).
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
