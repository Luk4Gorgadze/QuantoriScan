import subprocess
import sys


def run_migrations():
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Migration output:", result.stdout)
        if result.stderr:
            print("Migration errors:", result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Migration failed with error: {e.stderr}")
        return False


if __name__ == "__main__":
    success = run_migrations()
    if not success:
        sys.exit(1)
