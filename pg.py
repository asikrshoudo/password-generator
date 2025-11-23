import random
import string
import hashlib
import base64
import json
import time
from datetime import datetime

class UniversalPasswordGenerator:
    def __init__(self):
        self.generated_passwords = []
        self.password_history = []
        
    def generate_quantum_password(self, length=16, complexity="high"):
        """Generate strong password without external dependencies"""
        if complexity == "high":
            charset = string.ascii_letters + string.digits + "!@#$%^&*"
        elif complexity == "medium":
            charset = string.ascii_letters + string.digits
        else:  # low
            charset = string.ascii_lowercase + string.digits
        
        # Use system randomness
        password = ''.join(random.SystemRandom().choice(charset) for _ in range(length))
        
        # Ensure complexity requirements
        if complexity == "high":
            if not any(c in "!@#$%^&*" for c in password):
                password = self._inject_special_char(password)
            if not any(c.isupper() for c in password):
                password = self._inject_uppercase(password)
        
        return password
    
    def _inject_special_char(self, password):
        """Inject special character into password"""
        special_chars = "!@#$%^&*"
        pos = random.randint(0, len(password)-1)
        return password[:pos] + random.choice(special_chars) + password[pos+1:]
    
    def _inject_uppercase(self, password):
        """Inject uppercase letter into password"""
        pos = random.randint(0, len(password)-1)
        return password[:pos] + random.choice(string.ascii_uppercase) + password[pos+1:]
    
    def generate_mnemonic_password(self, word_count=4, separator="-", add_number=True):
        """Generate memorable password"""
        word_bank = [
            'red', 'blue', 'green', 'gold', 'silver', 'dragon', 'phoenix', 'tiger',
            'lion', 'eagle', 'wolf', 'bear', 'ocean', 'river', 'mountain', 'forest',
            'sun', 'moon', 'star', 'cloud', 'wind', 'fire', 'ice', 'earth',
            'king', 'queen', 'knight', 'wizard', 'dwarf', 'elf', 'giant', 'angel'
        ]
        
        words = [random.choice(word_bank) for _ in range(word_count)]
        words = [word.capitalize() for word in words]
        
        password = separator.join(words)
        
        if add_number:
            password += str(random.randint(10, 99))
        
        return password
    
    def generate_personal_password(self, base_info, pattern="mixed"):
        """Generate password from personal information"""
        # Create a hash base
        info_string = json.dumps(base_info, sort_keys=True)
        hash_base = hashlib.sha256(info_string.encode()).hexdigest()
        
        password = ""
        char_sets = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digit': string.digits,
            'special': "!@#$%^&*"
        }
        
        if pattern == "mixed":
            # Mix different character types
            for i in range(0, min(16, len(hash_base)), 2):
                chunk = hash_base[i:i+2]
                val = int(chunk, 16)
                
                if i % 4 == 0:  # lowercase
                    password += char_sets['lower'][val % 26]
                elif i % 4 == 1:  # uppercase
                    password += char_sets['upper'][val % 26]
                elif i % 4 == 2:  # digits
                    password += char_sets['digit'][val % 10]
                else:  # special
                    password += char_sets['special'][val % 8]
        
        elif pattern == "name_based":
            # Use names more directly
            names = [base_info.get('first_name', ''), base_info.get('last_name', '')]
            names = [name for name in names if name]
            
            if names:
                base = ''.join(names)
                # Interleave with hash
                for i in range(min(8, len(base))):
                    password += base[i]
                    if i < len(hash_base):
                        password += hash_base[i]
        
        return password[:16]  # Limit length
    
    def calculate_password_entropy(self, password):
        """Calculate password entropy bits"""
        char_pool = 0
        if any(c.islower() for c in password): char_pool += 26
        if any(c.isupper() for c in password): char_pool += 26
        if any(c.isdigit() for c in password): char_pool += 10
        if any(c in "!@#$%^&*" for c in password): char_pool += 10
        
        if char_pool == 0:
            return 0
        
        entropy = len(password) * (char_pool.bit_length())
        return entropy
    
    def check_password_strength(self, password):
        """Comprehensive password strength analysis"""
        score = 0
        feedback = []
        
        # Length
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        else:
            feedback.append("🔴 Password too short (min 8 characters)")
        
        # Character variety
        checks = {
            'uppercase': any(c.isupper() for c in password),
            'lowercase': any(c.islower() for c in password),
            'digits': any(c.isdigit() for c in password),
            'special': any(c in "!@#$%^&*" for c in password)
        }
        
        variety_count = sum(checks.values())
        score += variety_count
        
        if variety_count < 3:
            feedback.append("🟡 Add more character types")
        
        # Entropy
        entropy = self.calculate_password_entropy(password)
        if entropy > 80:
            score += 2
        elif entropy > 50:
            score += 1
        else:
            feedback.append("🟡 Low entropy - consider more randomness")
        
        # Common patterns
        weak_patterns = [
            '123', 'abc', 'qwer', 'password', 'admin', 'welcome'
        ]
        
        password_lower = password.lower()
        for pattern in weak_patterns:
            if pattern in password_lower:
                score -= 2
                feedback.append("🔴 Contains common weak pattern")
                break
        
        # Repeated characters
        if len(password) > len(set(password)) * 1.5:
            score -= 1
            feedback.append("🟡 Too many repeated characters")
        
        # Final rating
        if score >= 8:
            rating = "💪 VERY STRONG"
            color = "🟢"
        elif score >= 6:
            rating = "👍 STRONG"
            color = "🟢"
        elif score >= 4:
            rating = "🤔 MODERATE"
            color = "🟡"
        else:
            rating = "❌ WEAK"
            color = "🔴"
        
        return {
            'score': score,
            'rating': rating,
            'color': color,
            'entropy': entropy,
            'feedback': feedback,
            'length': len(password)
        }
    
    def bulk_generate(self, count=5, length=12, style="quantum"):
        """Generate multiple passwords"""
        passwords = []
        for i in range(count):
            if style == "quantum":
                pwd = self.generate_quantum_password(length)
            elif style == "mnemonic":
                pwd = self.generate_mnemonic_password()
            else:
                pwd = self.generate_quantum_password(length)
            
            strength = self.check_password_strength(pwd)
            passwords.append({
                'password': pwd,
                'strength': strength
            })
        
        return passwords
    
    def save_password_history(self, password, purpose=""):
        """Save password to history (in memory only)"""
        entry = {
            'password': password,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'purpose': purpose,
            'strength': self.check_password_strength(password)
        }
        self.password_history.append(entry)
        return entry

class PasswordGeneratorApp:
    def __init__(self):
        self.generator = UniversalPasswordGenerator()
        self.user_profile = {}
    
    def collect_user_info(self):
        """Collect optional user information for personalized passwords"""
        print("\n" + "="*50)
        print("🔐 PERSONAL INFORMATION (Optional)")
        print("="*50)
        print("Provide information for personalized passwords")
        print("Leave blank if you prefer random generation\n")
        
        self.user_profile['first_name'] = input("First name: ").strip()
        self.user_profile['last_name'] = input("Last name: ").strip()
        self.user_profile['birth_year'] = input("Birth year: ").strip()
        self.user_profile['nickname'] = input("Nickname: ").strip()
        self.user_profile['favorite_color'] = input("Favorite color: ").strip()
        self.user_profile['city'] = input("City: ").strip()
        
        # Filter out empty values
        self.user_profile = {k: v for k, v in self.user_profile.items() if v}
        
        if self.user_profile:
            print(f"\n✅ Collected {len(self.user_profile)} pieces of information")
        else:
            print("\nℹ️  Using completely random generation")
    
    def show_main_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("🚀 UNIVERSAL PASSWORD GENERATOR")
        print("="*50)
        print("1. 🔐 Generate Quantum Password")
        print("2. 🧠 Generate Memorable Password")
        print("3. 👤 Generate Personal Password")
        print("4. 📊 Check Password Strength")
        print("5. 📦 Bulk Generate Passwords")
        print("6. 🛠️  Password Workshop")
        print("7. 📝 Update Personal Info")
        print("8. 📋 Show Password History")
        print("9. 🚪 Exit")
        print("="*50)
    
    def generate_quantum_password_menu(self):
        """Quantum password generation menu"""
        print("\n=== QUANTUM PASSWORD GENERATOR ===")
        
        length = input("Length (12-32, default 16): ").strip()
        length = int(length) if length.isdigit() and 12 <= int(length) <= 32 else 16
        
        print("\nComplexity levels:")
        print("1. 🔥 High (Letters + Numbers + Special Characters)")
        print("2. 👍 Medium (Letters + Numbers)")
        print("3. 🎯 Low (Letters only)")
        
        comp_choice = input("Choose complexity (1-3, default 1): ").strip()
        complexity_map = {"1": "high", "2": "medium", "3": "low"}
        complexity = complexity_map.get(comp_choice, "high")
        
        password = self.generator.generate_quantum_password(length, complexity)
        self.display_password_result(password, "Quantum Password")
    
    def generate_mnemonic_password_menu(self):
        """Mnemonic password generation menu"""
        print("\n=== MEMORABLE PASSWORD GENERATOR ===")
        
        word_count = input("Word count (3-6, default 4): ").strip()
        word_count = int(word_count) if word_count.isdigit() and 3 <= int(word_count) <= 6 else 4
        
        separator = input("Separator (default -): ").strip() or "-"
        add_number = input("Add random number? (y/n, default y): ").strip().lower() != 'n'
        
        password = self.generator.generate_mnemonic_password(word_count, separator, add_number)
        self.display_password_result(password, "Memorable Password")
    
    def generate_personal_password_menu(self):
        """Personal password generation menu"""
        if not self.user_profile:
            print("\n❌ No personal information available!")
            print("Please update your personal info first (Option 7)")
            return
        
        print("\n=== PERSONAL PASSWORD GENERATOR ===")
        print("Using your personal information:")
        for key, value in self.user_profile.items():
            print(f"  • {key}: {value}")
        
        print("\nPattern styles:")
        print("1. 🔄 Mixed (Recommended)")
        print("2. 👤 Name-based")
        
        pattern_choice = input("Choose pattern (1-2, default 1): ").strip()
        pattern = "mixed" if pattern_choice != "2" else "name_based"
        
        password = self.generator.generate_personal_password(self.user_profile, pattern)
        self.display_password_result(password, "Personal Password")
    
    def check_strength_menu(self):
        """Password strength checking menu"""
        print("\n=== PASSWORD STRENGTH ANALYZER ===")
        password = input("Enter password to analyze: ").strip()
        
        if not password:
            print("❌ No password entered!")
            return
        
        result = self.generator.check_password_strength(password)
        
        print(f"\n{result['color']} STRENGTH ANALYSIS:")
        print(f"Rating: {result['rating']}")
        print(f"Score: {result['score']}/10")
        print(f"Length: {result['length']} characters")
        print(f"Entropy: {result['entropy']} bits")
        
        if result['feedback']:
            print(f"\n💡 RECOMMENDATIONS:")
            for feedback in result['feedback']:
                print(f"  {feedback}")
        
        # Offer to generate better version
        if result['score'] < 7:
            if input("\nGenerate stronger version? (y/n): ").lower() == 'y':
                stronger = self.generator.generate_quantum_password(max(12, len(password)))
                self.display_password_result(stronger, "Stronger Alternative")
    
    def bulk_generate_menu(self):
        """Bulk password generation menu"""
        print("\n=== BULK PASSWORD GENERATOR ===")
        
        count = input("How many passwords? (3-10, default 5): ").strip()
        count = int(count) if count.isdigit() and 3 <= int(count) <= 10 else 5
        
        print("\nPassword styles:")
        print("1. 🔐 Quantum (Most Secure)")
        print("2. 🧠 Memorable (Easy to Remember)")
        
        style_choice = input("Choose style (1-2, default 1): ").strip()
        style = "quantum" if style_choice != "2" else "mnemonic"
        
        print(f"\nGenerating {count} {style} passwords...\n")
        
        passwords = self.generator.bulk_generate(count, style=style)
        
        for i, pwd_info in enumerate(passwords, 1):
            pwd = pwd_info['password']
            strength = pwd_info['strength']
            print(f"{i}. {pwd} - {strength['color']} {strength['rating']}")
    
    def password_workshop_menu(self):
        """Interactive password workshop"""
        print("\n=== PASSWORD WORKSHOP ===")
        print("Test and improve your passwords interactively")
        
        while True:
            print("\n" + "-"*30)
            test_pwd = input("Enter a password to test (or 'back' to return): ").strip()
            
            if test_pwd.lower() == 'back':
                break
            
            if not test_pwd:
                continue
            
            result = self.generator.check_password_strength(test_pwd)
            
            print(f"\n{result['color']} ANALYSIS:")
            print(f"Rating: {result['rating']}")
            print(f"Score: {result['score']}/10")
            
            if result['feedback']:
                print("\n🔧 IMPROVEMENTS NEEDED:")
                for feedback in result['feedback']:
                    print(f"  • {feedback}")
            
            # Show similar strong passwords
            if result['score'] < 8:
                print(f"\n💡 STRONGER ALTERNATIVES:")
                for i in range(2):
                    strong_pwd = self.generator.generate_quantum_password(len(test_pwd) + 2)
                    strong_result = self.generator.check_password_strength(strong_pwd)
                    print(f"  {i+1}. {strong_pwd} - {strong_result['rating']}")
    
    def display_password_result(self, password, password_type):
        """Display generated password with analysis"""
        strength = self.generator.check_password_strength(password)
        
        print(f"\n🎉 {password_type} GENERATED!")
        print("="*40)
        print(f"🔐 PASSWORD: {password}")
        print(f"📊 LENGTH: {len(password)} characters")
        print(f"💪 STRENGTH: {strength['color']} {strength['rating']}")
        print(f"📈 SCORE: {strength['score']}/10")
        print(f"🎲 ENTROPY: {strength['entropy']} bits")
        
        # Save to history
        self.generator.save_password_history(password, password_type)
        
        # Copy suggestion
        print(f"\n💡 Tip: You can manually copy this password")
    
    def show_password_history(self):
        """Show password generation history"""
        if not self.generator.password_history:
            print("\n📭 No password history yet!")
            return
        
        print("\n=== PASSWORD HISTORY ===")
        for i, entry in enumerate(reversed(self.generator.password_history[-10:]), 1):
            print(f"\n{i}. {entry['password']}")
            print(f"   Type: {entry['purpose']}")
            print(f"   Time: {entry['timestamp']}")
            print(f"   Strength: {entry['strength']['rating']}")
    
    def run(self):
        """Main application loop"""
        print("🚀 WELCOME TO UNIVERSAL PASSWORD GENERATOR!")
        print("⭐ Works anywhere - No dependencies needed!")
        
        self.collect_user_info()
        
        while True:
            self.show_main_menu()
            choice = input("\nChoose option (1-9): ").strip()
            
            try:
                if choice == '1':
                    self.generate_quantum_password_menu()
                elif choice == '2':
                    self.generate_mnemonic_password_menu()
                elif choice == '3':
                    self.generate_personal_password_menu()
                elif choice == '4':
                    self.check_strength_menu()
                elif choice == '5':
                    self.bulk_generate_menu()
                elif choice == '6':
                    self.password_workshop_menu()
                elif choice == '7':
                    self.collect_user_info()
                elif choice == '8':
                    self.show_password_history()
                elif choice == '9':
                    print("\n🔒 Thank you for using Universal Password Generator!")
                    print("⭐ Your passwords were generated securely and locally!")
                    break
                else:
                    print("❌ Invalid choice! Please try again.")
            except Exception as e:
                print(f"❌ An error occurred: {e}")
            
            input("\nPress Enter to continue...")

# Run the application
if __name__ == "__main__":
    try:
        app = PasswordGeneratorApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")