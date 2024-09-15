#!/usr/bin/env python3
"""
Firefox Optimizer: Firefox Security & Privacy Optimizer
Version: 1.0
GitHub: https://github.com/Aerobit/FirefoxOptimizer

This script optimizes the security and privacy of Firefox by modifying user preferences.
It allows users to apply grouped optimization settings, backup current settings, restore from backup,
reset to default settings, and check for script updates.

Dependencies:
- None (uses only standard Python libraries)

Usage:
- Run the script and follow the on-screen menu options.
"""

import os
import sys
import shutil
import urllib.request
import json
import configparser

# Version number
__version__ = "1.0"

def banner():
    """
    Displays the script banner.
    """
    print("""
=============================================
           Firefox Optimizer v1.0
     Firefox Security & Privacy Optimizer
=============================================
    """)

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_firefox_profiles():
    """
    Retrieves a list of Firefox profile directories by parsing profiles.ini.

    Returns:
        list: A list of paths to Firefox profiles.
    """
    profiles = []

    # Define possible locations for profiles.ini
    profiles_ini_paths = []

    if sys.platform.startswith('linux'):
        # Standard installation
        standard_profiles_ini = os.path.expanduser('~/.mozilla/firefox/profiles.ini')
        # Snap installation
        snap_profiles_ini = os.path.expanduser('~/snap/firefox/common/.mozilla/firefox/profiles.ini')

        profiles_ini_paths.extend([standard_profiles_ini, snap_profiles_ini])
        base_paths = {
            standard_profiles_ini: os.path.expanduser('~/.mozilla/firefox'),
            snap_profiles_ini: os.path.expanduser('~/snap/firefox/common/.mozilla/firefox')
        }

    elif sys.platform == 'darwin':
        # macOS
        profiles_ini = os.path.expanduser('~/Library/Application Support/Firefox/profiles.ini')
        profiles_ini_paths.append(profiles_ini)
        base_paths = {
            profiles_ini: os.path.expanduser('~/Library/Application Support/Firefox')
        }

    elif sys.platform.startswith('win'):
        # Windows
        profiles_ini = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'profiles.ini')
        profiles_ini_paths.append(profiles_ini)
        base_paths = {
            profiles_ini: os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox')
        }
    else:
        print('Unsupported operating system.')
        sys.exit(1)

    found_profiles_ini = False

    for profiles_ini_path in profiles_ini_paths:
        if os.path.exists(profiles_ini_path):
            found_profiles_ini = True
            base_path = base_paths[profiles_ini_path]
            config = configparser.ConfigParser()
            config.read(profiles_ini_path)

            for section in config.sections():
                if section.startswith('Profile'):
                    path = config.get(section, 'Path', fallback=None)
                    is_relative = config.getint(section, 'IsRelative', fallback=1)
                    if path:
                        if is_relative:
                            profile_path = os.path.normpath(os.path.join(base_path, path))
                        else:
                            profile_path = os.path.normpath(path)
                        if os.path.exists(profile_path):
                            profiles.append(profile_path)
                        else:
                            print(f'Profile path does not exist: {profile_path}')
        else:
            continue  # Try the next possible profiles.ini path

    if not found_profiles_ini:
        print('No profiles.ini file found.')
        sys.exit(1)

    if not profiles:
        print('No Firefox profiles found.')
        sys.exit(1)
    else:
        print(f'Found {len(profiles)} Firefox profile(s).')

    return profiles

def display_main_menu():
    """
    Displays the main menu and options to the user.
    """
    clear_screen()
    banner()
    print("Firefox Optimizer - Firefox Security & Privacy Optimizer")
    print("Please select an option:")
    print("1. Apply optimization settings")
    print("2. Backup current settings")
    print("3. Restore settings from backup")
    print("4. Reset to default settings")
    print("5. Check for updates")
    print("q. Quit")

def display_category_menu(categories):
    """
    Displays the categories menu with available optimization groups.

    Args:
        categories (list): A list of category names.
    """
    clear_screen()
    print("Optimization Categories:")
    for idx, category in enumerate(categories, start=1):
        print(f"{idx}. {category}")
    print("\n0. Apply all categories")
    print("b. Go back to main menu")

def get_category_choices(categories):
    """
    Prompts the user to select categories to apply.

    Args:
        categories (list): A list of available categories.

    Returns:
        list or None: A list of selected indices or None to go back.
    """
    while True:
        display_category_menu(categories)
        choice = input("\nEnter the numbers of the categories to apply (comma-separated), 0 for all, or 'b' to go back: ").strip()
        if choice.lower() == 'b':
            return None
        elif choice == '0':
            return list(range(len(categories)))  # Apply all categories
        else:
            try:
                indices = [int(idx.strip()) - 1 for idx in choice.split(',')]
                if all(0 <= idx < len(categories) for idx in indices):
                    return indices
                else:
                    print("Invalid selection. Please choose valid category numbers.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")

def backup_settings(profiles):
    """
    Creates a backup of the current user.js settings for each profile.

    Args:
        profiles (list): A list of Firefox profile paths.
    """
    for profile in profiles:
        user_js = os.path.join(profile, 'user.js')
        backup_js = os.path.join(profile, 'user.js.backup')
        if os.path.exists(user_js):
            try:
                shutil.copy2(user_js, backup_js)
                print(f"Backup created for profile: {profile}")
            except Exception as e:
                print(f"Failed to create backup for profile {profile}: {e}")
        else:
            print(f"No user.js file found in profile: {profile}")

def restore_settings(profiles):
    """
    Restores settings from backup for each profile.

    Args:
        profiles (list): A list of Firefox profile paths.
    """
    for profile in profiles:
        backup_js = os.path.join(profile, 'user.js.backup')
        user_js = os.path.join(profile, 'user.js')
        if os.path.exists(backup_js):
            try:
                shutil.copy2(backup_js, user_js)
                print(f"Settings restored from backup for profile: {profile}")
            except Exception as e:
                print(f"Failed to restore settings for profile {profile}: {e}")
        else:
            print(f"No backup found for profile: {profile}")

def reset_to_default(profiles):
    """
    Resets settings to default by removing the user.js file for each profile.

    Args:
        profiles (list): A list of Firefox profile paths.
    """
    for profile in profiles:
        user_js = os.path.join(profile, 'user.js')
        if os.path.exists(user_js):
            try:
                os.remove(user_js)
                print(f"user.js removed, settings reset to default for profile: {profile}")
            except Exception as e:
                print(f"Failed to reset settings for profile {profile}: {e}")
        else:
            print(f"No user.js file to remove in profile: {profile}")

def update_script():
    """
    Checks for updates to the script on GitHub and updates if a new version is available.
    """
    print("\nChecking for updates...")
    repo_url = "https://api.github.com/repos/Aerobit/FirefoxOptimizer/releases/latest"
    try:
        with urllib.request.urlopen(repo_url) as response:
            if response.status != 200:
                print(f"Failed to check for updates. HTTP Status Code: {response.status}")
                return
            data = json.loads(response.read().decode())
            latest_version = data['tag_name']
            if latest_version.startswith('v'):
                latest_version = latest_version[1:]
            if latest_version != __version__:
                print(f"A new version ({latest_version}) is available.")
                assets = data.get('assets', [])
                if assets:
                    # Find the asset with the script name
                    download_url = None
                    for asset in assets:
                        if asset['name'] == 'firefox_optimizer.py':
                            download_url = asset['browser_download_url']
                            break
                    if download_url:
                        choice = input("Do you want to update now? (y/n): ").strip().lower()
                        if choice == 'y':
                            # Download and replace the current script
                            script_url = download_url
                            script_path = os.path.abspath(__file__)
                            try:
                                with urllib.request.urlopen(script_url) as response, open(script_path, 'wb') as out_file:
                                    shutil.copyfileobj(response, out_file)
                                print(f"Firefox Optimizer has been updated to version {latest_version}. Please restart the script.")
                                sys.exit(0)
                            except Exception as e:
                                print(f"Failed to download or replace the script: {e}")
                        else:
                            print("Update canceled.")
                    else:
                        print("Download URL for the script not found in the latest release.")
                else:
                    print("No downloadable assets found in the latest release.")
            else:
                print("You are using the latest version of Firefox Optimizer.")
    except Exception as e:
        print(f"Failed to check for updates: {e}")

def optimize_firefox():
    """
    Main function to execute the script logic.
    """
    clear_screen()
    banner()
    profiles = get_firefox_profiles()

    while True:
        display_main_menu()
        main_choice = input("\nEnter your choice: ").strip()
        if main_choice == '1':
            # Inform user that existing user.js files will be overwritten
            clear_screen()
            print("Note: Existing user.js files will be overwritten. A backup will be created as user.js.backup.")
            proceed = input("Do you want to continue? (y/n): ").strip().lower()
            if proceed != 'y':
                continue

            # Define optimization settings grouped by categories
            optimization_categories = {
                'Privacy Enhancements': [
                    {
                        'description': 'Enable First-Party Isolation',
                        'details': 'Prevents cross-site tracking by isolating cookies and other site data to the first-party domain.',
                        'settings': ['user_pref("privacy.firstparty.isolate", true);']
                    },
                    {
                        'description': 'Resist Fingerprinting',
                        'details': 'Makes the browser more resistant to fingerprinting techniques by minimizing uniquely identifying information.',
                        'settings': ['user_pref("privacy.resistFingerprinting", true);']
                    },
                    {
                        'description': 'Enable Global Privacy Control',
                        'details': 'Sends a signal to websites expressing your preference for privacy.',
                        'settings': ['user_pref("privacy.globalprivacycontrol.enabled", true);']
                    },
                    {
                        'description': 'Block Third-Party Cookies',
                        'details': 'Prevents third-party cookies used for cross-site tracking.',
                        'settings': [
                            'user_pref("network.cookie.cookieBehavior", 1);',
                            'user_pref("network.cookie.thirdparty.nonsecureSessionOnly", true);'
                        ]
                    },
                    {
                        'description': 'Disable Beacon API',
                        'details': 'Prevents tracking via the Beacon API.',
                        'settings': ['user_pref("beacon.enabled", false);']
                    },
                    {
                        'description': 'Disable Search Suggestions',
                        'details': 'Prevents search queries from being sent to search engines prematurely.',
                        'settings': ['user_pref("browser.search.suggest.enabled", false);']
                    },
                    {
                        'description': 'Enable Strict Referrer Policy',
                        'details': 'Limits the amount of information sent in the HTTP Referer header.',
                        'settings': ['user_pref("network.http.referer.XOriginPolicy", 2);']
                    },
                    {
                        'description': 'Disable Network Prediction',
                        'details': 'Prevents Firefox from predicting network actions to reduce unnecessary connections.',
                        'settings': ['user_pref("network.predictor.enable-hover-on-ssl", false);']
                    },
                    {
                        'description': 'Disable Search Suggestions in URL Bar',
                        'details': 'Prevents suggestions in the URL bar to enhance privacy.',
                        'settings': ['user_pref("browser.urlbar.suggest.searches", false);']
                    },
                    {
                        'description': 'Disable Telemetry Coverage',
                        'details': 'Disables telemetry coverage, preventing data collection.',
                        'settings': ['user_pref("toolkit.coverage.opt-out", true);']
                    },
                    {
                        'description': 'Disable Battery Status API',
                        'details': 'Prevents websites from accessing battery status to reduce fingerprinting.',
                        'settings': ['user_pref("dom.battery.enabled", false);']
                    },
                    {
                        'description': 'Disable Sensor APIs',
                        'details': 'Disables access to device sensors like gyroscope and accelerometer.',
                        'settings': ['user_pref("device.sensors.enabled", false);']
                    },
                    {
                        'description': 'Disable Network Information API',
                        'details': 'Prevents access to network information.',
                        'settings': ['user_pref("dom.netinfo.enabled", false);']
                    },
                    {
                        'description': 'Disable Resource Timing API',
                        'details': 'Prevents timing attacks by disabling the Resource Timing API.',
                        'settings': ['user_pref("dom.enable_resource_timing", false);']
                    },
                    {
                        'description': 'Disable Web Audio API',
                        'details': 'Prevents fingerprinting via the AudioContext API.',
                        'settings': ['user_pref("dom.webaudio.enabled", false);']
                    },
                    {
                        'description': 'Disable Virtual Reality Devices',
                        'details': 'Disables access to VR devices.',
                        'settings': ['user_pref("dom.vr.enabled", false);']
                    },
                    {
                        'description': 'Disable Gamepad API',
                        'details': 'Prevents websites from accessing gamepad devices.',
                        'settings': ['user_pref("dom.gamepad.enabled", false);']
                    },
                    {
                        'description': 'Disable Face Detection',
                        'details': 'Disables face detection capabilities.',
                        'settings': ['user_pref("camera.control.face_detection.enabled", false);']
                    },
                ],
                'Security Improvements': [
                    {
                        'description': 'Enable HTTPS Only Mode',
                        'details': 'Forces all connections to use HTTPS, enhancing security.',
                        'settings': ['user_pref("dom.security.https_only_mode", true);']
                    },
                    {
                        'description': 'Set Minimum TLS Version to 1.2',
                        'details': 'Enhances security by disallowing older, less secure TLS versions.',
                        'settings': ['user_pref("security.tls.version.min", 3);']
                    },
                    {
                        'description': 'Disable WebRTC (Prevent IP Leak)',
                        'details': 'Disables WebRTC to prevent your real IP address from leaking when using VPNs.',
                        'settings': [
                            'user_pref("media.peerconnection.enabled", false);',
                            'user_pref("media.peerconnection.use_document_iceservers", false);',
                            'user_pref("media.peerconnection.video.enabled", false);',
                            'user_pref("media.peerconnection.identity.timeout", 1);',
                            'user_pref("media.peerconnection.turn.disable", true);',
                            'user_pref("media.peerconnection.ice.no_host", true);'
                        ]
                    },
                    {
                        'description': 'Disable Geolocation',
                        'details': 'Prevents websites from requesting your physical location.',
                        'settings': [
                            'user_pref("geo.enabled", false);',
                            'user_pref("geo.provider.use_corelocation", false);',
                            'user_pref("geo.provider.ms-windows-location", false);',
                            'user_pref("geo.provider.use_gpsd", false);',
                            'user_pref("browser.search.geoip.url", "");',
                            'user_pref("permissions.default.geo", 2);'
                        ]
                    },
                    {
                        'description': 'Disable JavaScript in PDF Viewer',
                        'details': 'Enhances security by disabling JavaScript execution in the built-in PDF viewer.',
                        'settings': ['user_pref("pdfjs.enableScripting", false);']
                    },
                    {
                        'description': 'Disable Remote JAR Files',
                        'details': 'Prevents loading of Java ARchive (JAR) files from remote sources.',
                        'settings': ['user_pref("network.jar.block-remote-files", true);']
                    },
                    {
                        'description': 'Disable SSL Session Identifiers',
                        'details': 'Prevents tracking via SSL session identifiers.',
                        'settings': ['user_pref("security.ssl.disable_session_identifiers", true);']
                    },
                    {
                        'description': 'Disable Password Manager Autofill',
                        'details': 'Disables autofilling passwords to prevent unauthorized access.',
                        'settings': ['user_pref("signon.autofillForms", false);']
                    },
                    {
                        'description': 'Disable Third-Party Credentials',
                        'details': 'Prevents sending credentials to third-party sites.',
                        'settings': ['user_pref("network.http.sendRefererHeader", 0);']
                    },
                    {
                        'description': 'Disable Form Autofill Credit Cards',
                        'details': 'Prevents storing credit card information.',
                        'settings': ['user_pref("extensions.formautofill.creditCards.available", false);']
                    },
                    {
                        'description': 'Disable Microphone Access',
                        'details': 'Blocks all websites from accessing the microphone.',
                        'settings': ['user_pref("permissions.default.microphone", 2);']
                    },
                    {
                        'description': 'Disable Camera Access',
                        'details': 'Blocks all websites from accessing the camera.',
                        'settings': ['user_pref("permissions.default.camera", 2);']
                    },
                    {
                        'description': 'Disable Media Device Enumeration',
                        'details': 'Prevents websites from enumerating media devices.',
                        'settings': [
                            'user_pref("media.navigator.enabled", false);',
                            'user_pref("media.navigator.permission.disabled", true);',
                            'user_pref("media.navigator.video.enabled", false);'
                        ]
                    },
                    {
                        'description': 'Disable Speech Recognition',
                        'details': 'Disables speech recognition features.',
                        'settings': ['user_pref("media.webspeech.recognition.enable", false);']
                    },
                    {
                        'description': 'Disable Speech Synthesis',
                        'details': 'Disables speech synthesis features.',
                        'settings': ['user_pref("media.webspeech.synth.enabled", false);']
                    },
                    {
                        'description': 'Disable WebGL Debug Info',
                        'details': 'Prevents exposure of graphics card information.',
                        'settings': ['user_pref("webgl.enable-debug-renderer-info", false);']
                    },
                ],
                'Performance Optimizations': [
                    {
                        'description': 'Disable Prefetching and Speculative Connections',
                        'details': 'Prevents Firefox from making automatic connections to improve privacy and performance.',
                        'settings': [
                            'user_pref("network.prefetch-next", false);',
                            'user_pref("network.predictor.enabled", false);',
                            'user_pref("network.predictor.enable-prefetch", false);',
                            'user_pref("network.http.speculative-parallel-limit", 0);',
                            'user_pref("browser.urlbar.speculativeConnect.enabled", false);'
                        ]
                    },
                    {
                        'description': 'Disable DNS Prefetching',
                        'details': 'Prevents Firefox from pre-resolving domain names.',
                        'settings': [
                            'user_pref("network.dns.disablePrefetch", true);',
                            'user_pref("network.dns.disablePrefetchFromHTTPS", true);'
                        ]
                    },
                    {
                        'description': 'Disable IPv6',
                        'details': 'Disables IPv6 to prevent potential connectivity issues.',
                        'settings': ['user_pref("network.dns.disableIPv6", true);']
                    },
                    {
                        'description': 'Disable HTTP2',
                        'details': 'Disables HTTP2 for compatibility with some proxies.',
                        'settings': ['user_pref("network.http.spdy.enabled", false);']
                    },
                    {
                        'description': 'Disable HTTP Alternative Services',
                        'details': 'Prevents Firefox from making connections to alternative services.',
                        'settings': ['user_pref("network.http.altsvc.enabled", false);']
                    },
                    {
                        'description': 'Disable Link Prefetching',
                        'details': 'Prevents preloading of linked content.',
                        'settings': ['user_pref("network.http.speculative-parallel-limit", 0);']
                    },
                    {
                        'description': 'Disable Offline Cache',
                        'details': 'Prevents websites from storing data for offline use.',
                        'settings': ['user_pref("browser.cache.offline.enable", false);']
                    },
                    {
                        'description': 'Disable Browser Caching for SSL Content',
                        'details': 'Prevents caching of SSL content to enhance security.',
                        'settings': ['user_pref("browser.cache.disk_cache_ssl", false);']
                    },
                ],
                'Disable Telemetry and Data Collection': [
                    {
                        'description': 'Disable Telemetry and Data Collection',
                        'details': 'Prevents Firefox from sending usage and technical data to Mozilla.',
                        'settings': [
                            'user_pref("toolkit.telemetry.enabled", false);',
                            'user_pref("toolkit.telemetry.unified", false);',
                            'user_pref("toolkit.telemetry.archive.enabled", false);',
                            'user_pref("datareporting.healthreport.uploadEnabled", false);',
                            'user_pref("datareporting.policy.dataSubmissionEnabled", false);',
                            'user_pref("browser.ping-centre.telemetry", false);',
                            'user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);',
                            'user_pref("browser.newtabpage.activity-stream.telemetry", false);',
                            'user_pref("browser.discovery.enabled", false);',
                            'user_pref("browser.contentblocking.report.enabled", false);',
                            'user_pref("app.normandy.enabled", false);',
                            'user_pref("app.shield.optoutstudies.enabled", false);'
                        ]
                    },
                    {
                        'description': 'Disable Telemetry Pings',
                        'details': 'Prevents Firefox from sending additional telemetry pings.',
                        'settings': [
                            'user_pref("browser.ping-centre.telemetry", false);',
                            'user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);',
                            'user_pref("browser.newtabpage.activity-stream.telemetry", false);'
                        ]
                    },
                    {
                        'description': 'Disable Mozilla’s Extension Recommendations',
                        'details': 'Prevents Firefox from recommending extensions based on browsing behavior.',
                        'settings': ['user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr", false);']
                    },
                    {
                        'description': 'Disable Contextual Feature Recommender',
                        'details': 'Prevents Firefox from suggesting features based on usage.',
                        'settings': ['user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);']
                    },
                    {
                        'description': 'Disable Telemetry Coverage',
                        'details': 'Disables additional telemetry coverage pings.',
                        'settings': [
                            'user_pref("toolkit.coverage.opt-out", true);',
                            'user_pref("toolkit.coverage.endpoint.base", "");'
                        ]
                    },
                    {
                        'description': 'Disable Pocket',
                        'details': 'Disables Pocket integration in Firefox.',
                        'settings': ['user_pref("extensions.pocket.enabled", false);']
                    },
                    {
                        'description': 'Disable Normandy/Shield',
                        'details': 'Disables Normandy/Shield studies and experiments.',
                        'settings': [
                            'user_pref("app.normandy.enabled", false);',
                            'user_pref("app.normandy.api_url", "");'
                        ]
                    },
                ],
                'Miscellaneous Settings': [
                    {
                        'description': 'Disable Password Manager',
                        'details': 'Prevents Firefox from storing and autofilling passwords.',
                        'settings': [
                            'user_pref("signon.rememberSignons", false);',
                            'user_pref("signon.autofillForms", false);',
                            'user_pref("signon.formlessCapture.enabled", false);'
                        ]
                    },
                    {
                        'description': 'Disable Form Autofill',
                        'details': 'Prevents Firefox from saving and autofilling form data.',
                        'settings': [
                            'user_pref("browser.formfill.enable", false);',
                            'user_pref("extensions.formautofill.available", "off");',
                            'user_pref("extensions.formautofill.addresses.enabled", false);',
                            'user_pref("extensions.formautofill.creditCards.enabled", false);'
                        ]
                    },
                    {
                        'description': 'Disable Clipboard Events',
                        'details': 'Prevents websites from detecting clipboard copy/paste actions.',
                        'settings': ['user_pref("dom.event.clipboardevents.enabled", false);']
                    },
                    {
                        'description': 'Disable WebGL',
                        'details': 'Disables WebGL to prevent potential security risks and fingerprinting.',
                        'settings': ['user_pref("webgl.disabled", true);']
                    },
                    {
                        'description': 'Disable Captive Portal Detection',
                        'details': 'Prevents Firefox from making connections to detect captive portals.',
                        'settings': ['user_pref("network.captive-portal-service.enabled", false);']
                    },
                    {
                        'description': 'Clear Data on Shutdown',
                        'details': 'Configures Firefox to clear various types of data when it closes.',
                        'settings': [
                            'user_pref("privacy.clearOnShutdown.cache", true);',
                            'user_pref("privacy.clearOnShutdown.cookies", true);',
                            'user_pref("privacy.clearOnShutdown.downloads", true);',
                            'user_pref("privacy.clearOnShutdown.formdata", true);',
                            'user_pref("privacy.clearOnShutdown.history", true);',
                            'user_pref("privacy.clearOnShutdown.sessions", true);',
                            'user_pref("privacy.sanitize.sanitizeOnShutdown", true);'
                        ]
                    },
                    {
                        'description': 'Disable Middle Mouse Paste',
                        'details': 'Prevents pasting clipboard content on middle-click to avoid accidental data leakage.',
                        'settings': ['user_pref("middlemouse.contentLoadURL", false);']
                    },
                    {
                        'description': 'Disable Device Sensors',
                        'details': 'Disables access to device sensors like gyroscope and accelerometer.',
                        'settings': ['user_pref("device.sensors.enabled", false);']
                    },
                    {
                        'description': 'Disable Battery Status API',
                        'details': 'Prevents websites from accessing battery status to reduce fingerprinting.',
                        'settings': ['user_pref("dom.battery.enabled", false);']
                    },
                    {
                        'description': 'Disable Network Information API',
                        'details': 'Prevents access to network information.',
                        'settings': ['user_pref("dom.netinfo.enabled", false);']
                    },
                    {
                        'description': 'Disable Resource Timing API',
                        'details': 'Prevents timing attacks by disabling the Resource Timing API.',
                        'settings': ['user_pref("dom.enable_resource_timing", false);']
                    },
                    {
                        'description': 'Disable Web Audio API',
                        'details': 'Prevents fingerprinting via the AudioContext API.',
                        'settings': ['user_pref("dom.webaudio.enabled", false);']
                    },
                    {
                        'description': 'Disable Virtual Reality Devices',
                        'details': 'Disables access to VR devices.',
                        'settings': ['user_pref("dom.vr.enabled", false);']
                    },
                    {
                        'description': 'Disable Gamepad API',
                        'details': 'Prevents websites from accessing gamepad devices.',
                        'settings': ['user_pref("dom.gamepad.enabled", false);']
                    },
                    {
                        'description': 'Disable Face Detection',
                        'details': 'Disables face detection capabilities.',
                        'settings': ['user_pref("camera.control.face_detection.enabled", false);']
                    },
                ]
            }

            categories = list(optimization_categories.keys())
            selected_category_indices = get_category_choices(categories)
            if selected_category_indices is None:
                continue  # Go back to main menu

            # Compile selected settings
            selected_settings = []
            for idx in selected_category_indices:
                category = categories[idx]
                options = optimization_categories[category]
                for option in options:
                    selected_settings.extend(option['settings'])

            total_settings = len(selected_settings)
            for profile in profiles:
                user_js = os.path.join(profile, 'user.js')
                backup_js = os.path.join(profile, 'user.js.backup')

                # Backup existing user.js
                if os.path.exists(user_js):
                    try:
                        shutil.copy2(user_js, backup_js)
                        print(f"Existing user.js backed up to user.js.backup for profile: {profile}")
                    except Exception as e:
                        print(f"Failed to backup existing user.js for profile {profile}: {e}")
                        continue  # Skip to next profile
                else:
                    print(f"No existing user.js file to backup in profile: {profile}")

                # Write selected settings to user.js with progress display
                print(f"\nApplying settings to profile: {profile}")
                try:
                    with open(user_js, 'w') as f:
                        for index, setting in enumerate(selected_settings, start=1):
                            f.write(setting + '\n')
                            # Display progress
                            progress = (index / total_settings) * 100
                            print(f'Applying setting {index}/{total_settings} ({progress:.2f}%)', end='\r')
                    print(f'\nSettings applied to profile: {profile}')
                    # Verification
                    verify_settings(profile, selected_settings)
                except Exception as e:
                    print(f"An error occurred while writing to {user_js}: {e}")
                    continue  # Proceed to next profile

            input("\nPress Enter to return to the main menu...")

        elif main_choice == '2':
            clear_screen()
            backup_settings(profiles)
            input("\nPress Enter to return to the main menu...")
        elif main_choice == '3':
            clear_screen()
            restore_settings(profiles)
            input("\nPress Enter to return to the main menu...")
        elif main_choice == '4':
            clear_screen()
            reset_to_default(profiles)
            input("\nPress Enter to return to the main menu...")
        elif main_choice == '5':
            clear_screen()
            update_script()
            input("\nPress Enter to return to the main menu...")
        elif main_choice.lower() == 'q':
            print("Exiting Firefox Optimizer.")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")
            input("\nPress Enter to continue...")

def verify_settings(profile, selected_settings):
    """
    Verifies that the settings have been applied correctly.

    Args:
        profile (str): The path to the Firefox profile.
        selected_settings (list): The list of settings that were applied.
    """
    user_js = os.path.join(profile, 'user.js')
    try:
        with open(user_js, 'r') as f:
            applied_settings = f.readlines()

        missing_settings = []
        for setting in selected_settings:
            if setting.strip() + '\n' not in applied_settings:
                missing_settings.append(setting)

        if not missing_settings:
            print('All selected settings have been successfully applied and verified.')
        else:
            print('The following settings were not applied correctly:')
            for s in missing_settings:
                print(s)
    except Exception as e:
        print(f"Failed to verify settings for profile {profile}: {e}")

if __name__ == '__main__':
    optimize_firefox()
