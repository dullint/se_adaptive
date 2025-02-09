import subprocess


def main():
    subprocess.run(["streamlit", "run", "src/cai/app/main.py"], check=True)


if __name__ == "__main__":
    main()
