# Proxy Tester

A Python-based proxy testing tool that validates proxy servers, ranks them by speed, and saves working proxies in a format ready for use with Facebook automation tools.

## Features

- **Multi-threaded Testing**: Tests multiple proxies simultaneously for faster results
- **Speed Ranking**: Automatically sorts working proxies by response time (fastest first)
- **Anonymity Detection**: Identifies proxy anonymity levels (Transparent, Anonymous, Elite)
- **Speed Categorization**: Classifies proxies as Excellent, Good, Acceptable, Slow, or Poor
- **Environment Format Output**: Saves results in `FACEBOOK_PROXIES` environment variable format
- **Flexible Input**: Accepts proxies in various formats (IP:PORT, IP:PORT:USERNAME:PASSWORD)

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone or download this repository
2. Install the required dependency:

```bash
pip install requests
```

## Usage

You can provide proxies either interactively or from a file.

### 1. Interactive Input
Run the script without arguments:
```bash
python test_proxy.py
```
Paste your proxy list when prompted (one proxy per line):
```
161.35.70.249:8080
139.59.1.14:80
57.129.81.201:8080
138.68.60.8:80
```
Press Enter twice to finish input.

### 2. Load Proxies from a File
Prepare a text file (e.g., `proxies.txt`) with one proxy per line:
```
161.35.70.249:8080
139.59.1.14:80
57.129.81.201:8080
138.68.60.8:80
```
Run the script with the filename as an argument:
```bash
python test_proxy.py proxies.txt
```

The script will test all proxies and display results as described below.

## Output

The script provides:
- **Real-time testing status** with progress indication
- **Ranked list** of working proxies sorted by speed
- **Anonymity level** for each proxy
- **Speed category** (Excellent, Good, Acceptable, Slow, Poor)
- **Response time** in seconds

### Example Output:
```
🏆 Good Proxies (Fastest to Slowest):
1. 161.35.70.249:8080 | Elite | Excellent | 0.045s
2. 139.59.1.14:80 | Anonymous | Good | 0.234s
3. 57.129.81.201:8080 | Transparent | Acceptable | 0.567s
```

## Output File

Working proxies are automatically saved to `good_proxies.json` in the following format:
```json
FACEBOOK_PROXIES="161.35.70.249:8080,139.59.1.14:80,57.129.81.201:8080"
```

This format is ready to use as an environment variable for Facebook automation tools.

## Configuration

You can modify these settings in `test_proxy.py`:

- `TEST_URL`: The URL used to test proxies (default: "http://httpbin.org/ip")
- `TIMEOUT`: Request timeout in seconds (default: 10)
- `MAX_THREADS`: Maximum concurrent proxy tests (default: 30)

## Proxy Formats Supported

- **Basic**: `IP:PORT`
- **Authenticated**: `IP:PORT:USERNAME:PASSWORD`
- **HTTP/HTTPS**: Both protocols are supported

## Anonymity Levels

- **Elite**: Proxy doesn't reveal your real IP
- **Anonymous**: Proxy reveals it's a proxy but not your real IP
- **Transparent**: Proxy reveals both that it's a proxy and your real IP

## Speed Categories

- **Excellent**: < 0.1 seconds
- **Good**: 0.1 - 0.3 seconds
- **Acceptable**: 0.3 - 0.7 seconds
- **Slow**: 0.7 - 1.5 seconds
- **Poor**: > 1.5 seconds

## Error Handling

- Invalid proxies are automatically filtered out
- Network timeouts are handled gracefully
- Connection errors don't crash the application

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool. 