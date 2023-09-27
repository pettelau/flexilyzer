import subprocess
import json


def run_lighthouse(url: str):
    """Function for running the lighthouse command in cmd line"""
    output_file = (
        f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.json"
    )

    command = [
        "lighthouse",
        url,
        "--output=json",
        f"--output-path={output_file}",
        '--chrome-flags="--headless"',
    ]
    subprocess.run(command)
    return output_file


def read_lighthouse_report(file_path: str):
    """Function for reading the newly generated report"""
    with open(file_path, "r") as file:
        report = json.load(file)
    return report


def lighthouse_analyzer(project_id):
    # In future, url should come from rabbitmq payload
    url = "https://tsffbet.no"

    # Run lighthouse and get file name in return
    output_file = run_lighthouse(url)

    # Load newly generated report
    report: json = read_lighthouse_report(output_file)

    cleaned_report = {
        "fcp": report["audits"]["first-contentful-paint"],
        "viewport": report["audits"]["viewport"],
    }
    return cleaned_report


if __name__ == "__main__":
    report = lighthouse_analyzer(1)

    print(report)
