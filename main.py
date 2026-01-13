import subprocess, time

def run_adb(serial, args, check=False):
    cmd = ["adb", "-s", serial] + args
    return subprocess.run(cmd, text=True, check=check)

def tap(serial, x, y):
    run_adb(serial, ["shell", "input", "tap", str(x), str(y)])

def text(serial, t):
    safe = t.replace(" ", "%s")
    run_adb(serial, ["shell", "input", "text", safe])

def open_firefox(serial):
    run_adb(serial, [
        "shell", "monkey",
        "-p", "org.mozilla.firefox",
        "-c", "android.intent.category.LAUNCHER",
        "1"
    ])

def open_url_in_firefox(serial, url):
    run_adb(serial, [
        "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", url
    ])

def get_model(serial):
    out = subprocess.check_output(
        ["adb", "-s", serial, "shell", "getprop", "ro.product.model"],
        text=True
    ).strip()
    return out

def get_devices():
    result = subprocess.check_output(["adb", "devices"], text=True)
    lines = result.strip().splitlines()[1:]
    devices = []
    for line in lines:
        if "\tdevice" in line:
            devices.append(line.split("\t")[0])
    return devices

def install_cookie_extension(serial):
    open_url_in_firefox(serial, "https://addons.mozilla.org/firefox/addon/cookie-editor")
    time.sleep(3)
    tap(serial, 523, 1794)
    time.sleep(2)
    tap(serial, 871, 1958)
    time.sleep(2)
    tap(serial, 901, 1963)

def import_cookie(serial):
    open_url_in_firefox(serial, "https://tiktok.com/profile")
    time.sleep(2)
    tap(serial, 1007, 157)
    tap(serial, 523, 1071)
    tap(serial, 565, 359)
    time.sleep(1)
    tap(serial, 406, 1984)
    time.sleep(1)
    tap(serial, 680, 1981)

    # After paste value -> click import
    # tap(serial, 817, 1104)

def run_flow(serial):
    model = get_model(serial)
    print(f"🚀 Running on {serial} ({model})")

    open_firefox(serial)
    time.sleep(2)

    install_cookie_extension(serial)
    time.sleep(2)

    import_cookie(serial)
    time.sleep(2)

# if __name__ == "__main__":
#     devices = get_devices()

#     if not devices:
#         print("❌ No authorized devices found (check USB debugging / allow prompt).")
#     else:
#         print(f"✅ Found {len(devices)} devices:")
#         for d in devices:
#             print(" -", d)

#         for d in devices:
#             run_flow(d)
