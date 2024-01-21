# Custom INI Data Processor

This repository contains a Python script designed to read and process INI configuration files from CSP ( Custom Shaders Patch ) based on a structured JSON template. It's particularly useful for extracting and organizing data from complex configuration files into a more manageable format.

Realised thanks to the repository Wiki :
https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki

CSP Last Update for the script : v0.2.2

## Overview

The script `process_ini.py` reads data from INI files, compares it against a predefined JSON template, and extracts specific information. This is particularly useful in scenarios where configuration files are dense and need to be decoded into a more readable and usable format.

## Features

- Reads and processes INI files.
- Uses JSON templates for flexible and customizable data extraction.
- Supports nested categories and sub-categories in templates.
- Handles special conditions for entry matching.
- Outputs processed data in JSON format for easy use in other applications.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/TheYakuzo/AssettoCorsa_CSP_Parser
cd AssettoCorsa_CSP_Parser
```

## Usage

1. Place your INI file and JSON template in the project directory.
2. Run the script with Python:

   ```bash
   python3 csp_parser.py
   ```

Check the output, which will be printed in the console and can be redirected to a file if needed.

## Customization

1. Edit ext_config.ini to match your specific INI file structure.
2. Modify car_csp.json (or create a new JSON template) to define the structure and specific data points you wish to extract from the INI file.

## Contributing

Contributions to improve the script are welcome. Please feel free to fork the repository and submit pull requests.

## Script Output

```json
{
    "fuel": {
        "gasoline_engine": true
    },
    "instruments": {
        "analog_instruments": {
            "time": true
        }
    },
    "audio": {
        "audio_volume": {
            "engine_exterior": "1.5",
            "engine_interior": "0.6",
            "gear_exterior": "1",
            "gear_interior": "1",
            "body_work": "1",
            "wind": "1",
            "dirt": "1",
            "down_shift": "1",
            "horn": "1",
            "gear_grind": "1",
            "backfire_ext": "1",
            "backfire_int": "1",
            "transmission": "1",
            "limiter": "1",
            "turbo": "1"
        }
    },
    "exhaust_smoke": true,
    "lightning": {
        "self_lightning": {
            "headlights": true
        },
        "lights": {
            "exterior": {
                "headlights": true,
                "beam": {
                    "high": true
                },
                "brakes": {
                    "rear": true
                },
                "turnsignals": {
                    "front_left": true,
                    "front_right": true,
                    "rear_left": true,
                    "rear_right": true,
                    "side_left": true,
                    "side_right": true
                },
                "informations": {
                    "tyre_pressure": {
                        "low": true
                    }
                },
                "reversing": true
            },
            "interior": {
                "handbrake": true,
                "abs_inaction": true,
                "tc": true,
                "tc_inaction": true,
                "turnsignals": {
                    "front_left": true,
                    "front_right": true
                }
            }
        }
    },
    "miscellaneous": {
        "glass": true
    },
    "wobbly_wipers": true,
    "wipers_trace": {
        "left": true,
        "right": true
    },
    "navigation": {
        "android_auto": true,
        "gps": true
    }
}
```
