#!/usr/bin/env python

import datetime
import socket
import os
import psutil
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_system_info():
    """
    HTTP endpoint to return hostname, uptime, CPU count, and total memory.
    """
    try:
        hostname = socket.gethostname()

        uptime = get_uptime()

        cpu_count = os.cpu_count()

        total_memory_bytes = psutil.virtual_memory().total
        total_memory_gb = round(total_memory_bytes / (1024**3), 2)

        system_info = {
            "hostname": hostname,
            "uptime": uptime,
            "cpu_count": cpu_count,
            "total_memory_gb": total_memory_gb,
        }

        return jsonify(system_info)

    except Exception as e:
        print(f"An error occurred: {e}")
        return (
            jsonify(
                {"error": "Could not retrieve system information", "details": str(e)}
            ),
            500,
        )


def get_uptime():
    total_seconds = (
        datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    ).total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
