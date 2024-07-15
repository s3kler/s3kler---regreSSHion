# s3kler - regreSSHion
This tool checks the version of OpenSSH running on specified hosts and ports and determines if they are potentially vulnerable.

## Features

- Connects to SSH servers and retrieves their version information
- Checks the OpenSSH version against known vulnerable versions
- Supports multiple hosts and ports

## Requirements

- Python 3.x
- `colorama` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/openssh-version-checker.git
    cd openssh-version-checker
    ```

2. Install the required Python package:

    ```bash
    pip install colorama
    ```

## Usage

1. Create a file containing the list of hostnames or IP addresses, one per line. For example, `hosts.txt`:

    ```
    host1.example.com
    host2.example.com
    192.168.1.1
    ```

2. Run the script with the filename and ports as arguments:

    ```bash
    python ssh_version_check.py <filename> <ports>
    ```

    Example:

    ```bash
    python ssh_version_check.py hosts.txt 22,2222
    ```

    This will check the SSH version on the hosts specified in `hosts.txt` on ports 22 and 2222.
