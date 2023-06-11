import argparse
import json
import os
import yaml
from src.asgi import app

parser = argparse.ArgumentParser(
    prog="extract-openapi.py",
    description="Extract OpenAPI specs from FastAPI app into openapi.yml and openapi.json ",
)
parser.add_argument("output_dir", help="Output directory", default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    openapi = app.openapi()
    version = openapi.get("openapi", "unknown version")

    print(f"writing openapi spec v{version} to {args.output_dir}")

    os.makedirs(args.output_dir, exist_ok=True)

    json_file = os.path.join(args.output_dir, "openapi.json")
    with open(json_file, "w") as f:
        json.dump(openapi, f, indent=2)

    yaml_file = os.path.join(args.output_dir, "openapi.yml")
    with open(yaml_file, "w") as f:
        yaml.dump(openapi, f, sort_keys=False)

    print(f"spec written to {args.output_dir}")
