# USB/SSD Storage Device Validation Framework

Welcome to the USB/SSD Storage Device Validation Framework, a tool designed to automate the testing of USB and SSD storage devices. This framework allows you to simulate real-world usage and test the reliability, performance, and fault tolerance of your storage devices.

![Project Logo](https://via.placeholder.com/150)

## Features

- **Performance Testing**: Validate read/write speeds and consistency under load.
- **Data Integrity**: Checksum validation to ensure no data corruption.
- **Endurance Testing**: Assess device performance after extensive use.
- **Fault Simulation**: Inject faults like power loss to test recovery.
- **Reporting System**: Generate and display test results with a real-time dashboard.

## Project Structure

- **Core Modules**
  - `config_manager.py`: Manages configuration settings.
  - `device_manager.py`: Handles device validation and information.
  - `test_framework.py`: Orchestrates testing.

- **Testing Modules**
  - Simulates tests for performance, integrity, and fault conditions.

- **Utilities**
  - `logger.py`: Logs activities and errors.

- **Reporting**
  - `report_generator.py`: Generates HTML and CSV reports.

## Installation

### Prerequisites

- Python 3.7+
- Pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### List Available Devices

```bash
python main.py --list-devices
```

### Run Performance Test

```bash
python main.py --device D: --test performance
```

### Dry Run

```bash
python main.py --device D: --dry-run
```

### View Reports

- Reports are stored in the `reports` directory as both HTML and CSV.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

- **Author**: Amogh DP
- **Email**: amogh@example.com

---

Made with ❤️ by Amogh DP

