
# FirefoxOptimizer

**FirefoxOptimizer** is a Python tool designed to optimize the security, privacy, and performance of Mozilla Firefox by automatically adjusting its configuration settings.

This tool simplifies the process of managing advanced `about:config` preferences, particularly for users who want to maximize their privacy and security without manually editing the configuration settings themselves.

## Features

- **Privacy Enhancements**: Disable telemetry, tracking, and data collection features, block third-party cookies, and resist browser fingerprinting.
- **Security Optimizations**: Strengthen web security by forcing HTTPS, disabling WebRTC (to prevent IP leaks), and blocking insecure connections.
- **Performance Improvements**: Fine-tune browser caching and predictive behaviors for better performance.
- **Automation**: Automatically modify the Firefox configuration using `user.js`, no manual intervention needed.

## Requirements

- Python 3.x
- Mozilla Firefox installed

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Aerobit/FirefoxOptimizer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd FirefoxOptimizer
   ```

3. Run the optimizer script to apply the optimizations:

   ```bash
   python3 firefox_optimizer.py
   ```

## Usage

Once you run the script, a menu will guide you through various actions, including applying optimization settings, backing up current settings, restoring from backup, resetting to default Firefox settings, and checking for script updates.

1. **Apply Optimizations**: Modify your Firefox profiles with security, privacy, and performance improvements by selecting from categorized optimizations.
2. **Backup Settings**: Automatically backup the current `user.js` configuration before any changes are made.
3. **Restore Settings**: Restore previously backed-up settings if needed.
4. **Reset to Default**: Completely reset your Firefox configuration by removing the `user.js` file.
5. **Update Script**: Automatically check for updates to the optimizer from the GitHub repository.

## Optimization Categories

- **Privacy Enhancements**: Prevent cross-site tracking, enable first-party isolation, disable telemetry, disable beacon API, resist fingerprinting, etc.
- **Security Improvements**: Force HTTPS connections, disable WebRTC, set minimum TLS version, disable geolocation services, disable JavaScript in the PDF viewer, block media devices, etc.
- **Performance Optimizations**: Disable speculative connections, DNS prefetching, HTTP2, IPv6, and offline caching.
- **Disable Telemetry**: Turn off all telemetry and data reporting features within Firefox to prevent the browser from sending any data back to Mozilla or third-party services.
- **Miscellaneous Settings**: Disable password autofill, form autofill, WebGL, clipboard events, and more.

### Example

Here is a simple example of running the script:

```bash
python3 firefox_optimizer.py
```

Select option `1` to apply optimization settings, and then choose the categories you want to apply, such as Privacy or Security settings.

## Backup and Restore

- **Backup**: Before applying any changes, the script will automatically create a backup of your `user.js` file and save it as `user.js.backup`.
- **Restore**: If you need to revert the changes, you can easily restore the backup by selecting the `Restore from Backup` option in the menu.

## Update Mechanism

The script can check for updates from its GitHub repository. When a new version is available, the user will be prompted to download and replace the current version.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or feedback, feel free to open an issue on the repository.

---

**FirefoxOptimizer** is designed to help users protect their privacy and improve browser performance by automatically applying well-tested Firefox optimizations.
