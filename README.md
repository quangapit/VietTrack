VietTrack 🇻🇳

Multi-carrier Parcel Tracking for Vietnam

A lightweight Python CLI tool to track shipments across multiple Vietnamese shipping carriers.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python) !Platform !License !Open Source

✨ Introduction

VietTrack is a simple and lightweight parcel tracking tool written in Python.

It allows you to track shipments from multiple Vietnamese shipping carriers using a single command-line interface.

No need to visit multiple tracking websites. Just provide your tracking number and VietTrack will automatically detect the carrier and retrieve shipment history whenever supported.


## 🚀 Features

- 🔍 **Automatic Carrier Detection**
  Automatically detect shipping carriers based on tracking number patterns.
- 📦 **Multi-carrier Tracking**
  Support multiple Vietnamese shipping services.
- 📋 **Tracking History**
  Display detailed shipment tracking events.
- 📍 **Location Information**
  Show shipment locations when available.
- 📱 **Phone Verification**
  Support phone verification for certain carriers.
- 🌐 **Direct Tracking Links**
  Open carrier tracking websites when direct tracking is unavailable.
- ⚡ **Lightweight**
  Built using Python standard libraries without additional dependencies.
- 💻 **CLI Interface**
  Simple and easy-to-use command-line interface.
- 🔓 **Open Source**
  Free to use, modify, and contribute.
  
- 📦 Supported Carriers

# VietTrack supports the following shipping carriers:
- Carrier	Support	Tracking Method
- SPX Express	✅	Direct API
- LEX	✅	Direct API
- GHN	✅	Direct API / Phone Verification
- J&T Express	✅	Direct API / Website
- Vietnam Post	🔗	Official Tracking Website
- Viettel Post	🔗	Tracking Website
- Ninja Van	🔗	Tracking Website
- GHTK	🔗	Tracking Website
- TikTok Express	⚠️	Public tracking unavailable

# Legend:

- ✅ Direct tracking supported.
- 🔗 Redirects to the carrier's tracking page.
- ⚠️ Public tracking is currently unavailable.

Carrier availability and tracking methods may change over time.

🛠️ Requirements
Python 3.8 or newer.
Internet connection.

No third-party Python packages are required.

📥 Installation
1. Clone the repository
```hash
git clone https://github.com/quangapit/VietTrack.git
```
3. Navigate to the project directory
```bash
cd VietTrack
```
4. Run VietTrack
```bash
python track.py SPXVN123456789
```

That's it! No additional dependencies are required.

💡 Usage
Basic Tracking

Simply provide your tracking number:

```bash
python track.py SPXVN123456789
```

VietTrack will automatically identify the carrier and retrieve tracking information.

Track with Phone Verification

Some carriers require the last four digits of the recipient's phone number.

GHN:

```bash
python track.py GHN123456789 1234
```

J&T Express:

```bash
python track.py JT1234567890 1234
```

Replace 1234 with the actual last four digits of the phone number associated with the shipment.

Open Tracking Website Automatically

For carriers that require JavaScript or CAPTCHA verification:

```bash
python track.py TRACKING_NUMBER --open
```

VietTrack will open the corresponding tracking website in your default browser when a matching tracking format is available.

List Supported Carriers
```bash
python track.py --track
```

Example output:

text
Hãng vận chuyển được hỗ trợ:
  SPX
  LEX
  GHN
  JTEXPRESS
  vnPost
  ViettelPost
  Ninja Van
  GHTK
  TikTok Express

📋 Example Output
text
Hãng: SPX | Mã: SPXVN123456789

Trạng thái: Đang vận chuyển

10:30 13/11/2026  Đơn hàng đã đến kho phân loại
   Hồ Chí Minh

08:15 13/11/2026  Đơn hàng đang được vận chuyển

20:45 12/11/2026  Đơn hàng đã được lấy thành công
   Kho lấy hàng


The output above is for demonstration purposes only.

# 📂 Project Structure
text
VietTrack/
│
├── track.py

⚙️ How It Works

VietTrack uses regular expressions to identify shipping carriers based on tracking number formats.

Depending on the carrier, the tool:

Detects the carrier automatically.
Sends a tracking request to an available tracking endpoint.
Retrieves shipment tracking events.
Parses tracking timestamps, descriptions, and locations.
Sorts tracking events by time.
Displays the shipment history in the terminal.

If direct tracking is unavailable, VietTrack attempts to use a fallback tracking service or provides a tracking website when the tracking number matches a supported format.

🔐 Privacy & Security
Tracking requests are sent to external carrier APIs or tracking services.
Phone verification digits may be transmitted when required.
VietTrack does not maintain its own shipment database.
Avoid sharing tracking numbers and personal information publicly.
⚠️ Disclaimer

VietTrack is an independent open-source project.

This project is not affiliated with, endorsed by, or officially connected to:

SPX Express
LEX
GHN
J&T Express
Vietnam Post
Viettel Post
Ninja Van
GHTK
TikTok

All trademarks and company names belong to their respective owners.

This project uses publicly accessible tracking endpoints and third-party tracking services where available. These services may change, restrict access, require verification, or become unavailable without notice.

Users are responsible for complying with the terms of service and applicable policies of the respective carriers.

🤝 Contributing

Contributions are welcome!

If you want to improve VietTrack, add support for new carriers, or fix bugs, feel free to contribute.

How to Contribute
Fork this repository.
Create a new branch.
```bash
git checkout -b feature/new-carrier
```
Make your changes.
Commit your changes.
```bash
git commit -m "Add support for new carrier"
```
Push your branch.
```bash
git push origin feature/new-carrier
```
Open a Pull Request.

We appreciate every contribution!

🗺️ Roadmap
Automatic carrier detection.
Multi-carrier tracking.
Tracking history display.
Phone verification support.
Direct tracking website support.
More Vietnamese shipping carriers.
Improved error handling.
JSON output mode.
REST API support.
Web dashboard.
Unit tests.
⭐ Support the Project

If you find VietTrack useful, please consider giving this repository a ⭐ Star on GitHub.

Your support helps the project reach more developers and encourages further development.

📄 License

This project is intended to be distributed under the MIT License.

See the LICENSE file for details.

<p align="center">

Made with ❤️ in Vietnam

VietTrack – One Tool. All Your Shipments.

</p>
