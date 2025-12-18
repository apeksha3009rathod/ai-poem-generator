import requests  # type: ignore
import time

API_URL = "http://127.0.0.1:8088/api/v1/poem"


def typing_animation(text: str, delay: float = 0.03):
    """Print text with a typing animation."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def main():
    print("=" * 60)
    typing_animation("🌟 Welcome to the Poetic CLI Companion 🌟", 0.05)
    print("=" * 60)
    typing_animation("Type anything and receive a poetic response.")
    typing_animation("Type 'exit' to quit.\n")

    while True:
        user_input = input("💭 You: ").strip()

        if user_input.lower() in {"exit", "quit", "bye"}:
            typing_animation("\n✨ The poet bows and departs... ✨")
            break

        if not user_input:
            continue

        try:
            response = requests.post(
                API_URL,
                json={"input_text": user_input},
                timeout=30,
            )
            response.raise_for_status()
        except Exception as exc:
            print("Failed to reach backend:", exc)
            continue

        poem = response.json()["poem"]

        print("\n📜 Poet:")
        typing_animation(poem, delay=0.02)
        print("-" * 60)


if __name__ == "__main__":
    main()
