# 🔒 Universal Password Generator | pg.py

**Project Link:** [https://github.com/asikrshoudo/password-generator.git](https://github.com/asikrshoudo/password-generator.git)

**A complete, dependency-light, and feature-rich Python solution for generating highly secure, memorable, and personalized passwords, featuring advanced strength analysis and an interactive CLI.**

---

## 🌟 Key Features

| Feature | Description | Security Method |
| :--- | :--- | :--- |
| **Quantum Generation** | Generates extremely secure, high-entropy passwords with adjustable length and complexity. | Uses Python's built-in `random.SystemRandom()` for cryptographically secure random number generation. |
| **Mnemonic Passphrases** | Creates memorable passwords using a curated word bank and separators (e.g., `King-Tiger-Ocean25`). | Focuses on length and character set diversity for high entropy while remaining human-readable. |
| **Personalized Passwords** | Generates unique passwords derived from a **SHA256 hash** of optional user-provided personal details. | Ensures the derived password is unique to the user's info, *without storing the sensitive details*. |
| **Advanced Strength Check** | Provides a comprehensive score, rating, and calculates **Shannon Entropy** (in bits) for any password. | Detects weak patterns and offers feedback for immediate improvement. |
| **Interactive CLI** | User-friendly, menu-driven interface (`PasswordGeneratorApp`) for seamless operation. | |

## 🛠️ Installation & Execution

This project is built using only standard Python libraries. No external packages are required!

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/asikrshoudo/password-generator.git](https://github.com/asikrshoudo/password-generator.git)
    cd password-generator
    ```

2.  **Run the main file (`pg.py`):**
    ```bash
    python pg.py
    ```

## 💡 Usage

The application starts with an optional information collection phase and then displays the main menu, offering various generation and analysis tools:

### Password Strength Calculation (Core Logic)

The core strength analysis relies on calculating **Shannon Entropy** ($E$) to measure the randomness of the password:

$$
E = L \times \log_2(N)
$$

* $L$ = Length of the password.
* $N$ = Size of the character pool (e.g., 90+ if it includes uppercase, lowercase, digits, and special characters).

A higher entropy score (typically **> 80 bits**) indicates a more secure, brute-force resistant password.

## ⚙️ Project Structure

The project is encapsulated within two main classes in `pg.py`:

* **`UniversalPasswordGenerator`**: Handles all generation methods (`quantum`, `mnemonic`, `personal`), strength analysis, and entropy calculation.
* **`PasswordGeneratorApp`**: Manages the interactive command-line interface (CLI) and user workflow.

## 🤝 Contribution Guidelines

Contributions are highly encouraged! Whether it's fixing bugs, improving the word bank, or suggesting new complexity metrics, please feel free to contribute.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/NewFeature`).
3.  Commit your Changes (`git commit -m 'Implement New Feature'`).
4.  Push to the Branch (`git push origin feature/NewFeature`).
5.  Open a detailed **Pull Request**.

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

## 📧 Contact & Author

**Author:** Ashikur Sheikh Shoudo

* **Public Email:** ask.shoudo@gmail.com
* **GitHub/Socials:** [@asikrshoudo](https://github.com/asikrshoudo)
* **Project Link:** [https://github.com/asikrshoudo/password-generator.git](https://github.com/asikrshoudo/password-generator.git)
