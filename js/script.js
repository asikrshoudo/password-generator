// Character sets
const charSets = {
    uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    lowercase: 'abcdefghijklmnopqrstuvwxyz',
    numbers: '0123456789',
    symbols: '!@#$%^&*'
};

// DOM Elements
const lengthSlider = document.getElementById('length');
const lengthValue = document.getElementById('length-value');
const generateBtn = document.getElementById('generate');
const passwordDisplay = document.getElementById('password');
const copyBtn = document.getElementById('copy-btn');
const refreshBtn = document.getElementById('refresh-btn');
const batchCount = document.getElementById('batch-count');
const batchGenerateBtn = document.getElementById('batch-generate');
const passwordList = document.getElementById('password-list');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// Checkbox elements
const uppercaseCheck = document.getElementById('uppercase');
const lowercaseCheck = document.getElementById('lowercase');
const numbersCheck = document.getElementById('numbers');
const symbolsCheck = document.getElementById('symbols');
const customInput = document.getElementById('custom');

// Strength meter elements
const strengthLabel = document.getElementById('strength-label');
const meterFill = document.getElementById('meter-fill');
const entropyDisplay = document.getElementById('entropy');
const crackTimeDisplay = document.getElementById('crack-time');

// Update length value display
lengthSlider.addEventListener('input', () => {
    lengthValue.textContent = lengthSlider.value;
    updateStrengthMeter();
});

// Generate password function
function generatePassword() {
    let characters = '';
    let password = '';
    
    // Build character pool based on selections
    if (uppercaseCheck.checked) characters += charSets.uppercase;
    if (lowercaseCheck.checked) characters += charSets.lowercase;
    if (numbersCheck.checked) characters += charSets.numbers;
    if (symbolsCheck.checked) characters += charSets.symbols;
    
    // Add custom characters
    const customChars = customInput.value.trim();
    if (customChars) {
        characters += customChars;
    }
    
    // Check if at least one character set is selected
    if (characters.length === 0) {
        showToast('Please select at least one character type!', 'error');
        return 'No character types selected';
    }
    
    const length = parseInt(lengthSlider.value);
    
    // Generate password
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        password += characters[randomIndex];
    }
    
    // Ensure at least one character from each selected set
    password = ensureCharacterSets(password, characters);
    
    return password;
}

function ensureCharacterSets(password, allCharacters) {
    const length = password.length;
    let newPassword = password.split('');
    
    // Track which character sets are selected
    const sets = [];
    if (uppercaseCheck.checked) sets.push('uppercase');
    if (lowercaseCheck.checked) sets.push('lowercase');
    if (numbersCheck.checked) sets.push('numbers');
    if (symbolsCheck.checked) sets.push('symbols');
    
    // For each selected set, ensure at least one character is present
    sets.forEach(set => {
        let hasCharFromSet = false;
        
        switch(set) {
            case 'uppercase':
                hasCharFromSet = /[A-Z]/.test(newPassword.join(''));
                break;
            case 'lowercase':
                hasCharFromSet = /[a-z]/.test(newPassword.join(''));
                break;
            case 'numbers':
                hasCharFromSet = /[0-9]/.test(newPassword.join(''));
                break;
            case 'symbols':
                hasCharFromSet = /[!@#$%^&*]/.test(newPassword.join(''));
                break;
        }
        
        if (!hasCharFromSet) {
            // Replace a random position with a character from the missing set
            const randomIndex = Math.floor(Math.random() * length);
            let replacementChar;
            
            switch(set) {
                case 'uppercase':
                    replacementChar = charSets.uppercase[Math.floor(Math.random() * charSets.uppercase.length)];
                    break;
                case 'lowercase':
                    replacementChar = charSets.lowercase[Math.floor(Math.random() * charSets.lowercase.length)];
                    break;
                case 'numbers':
                    replacementChar = charSets.numbers[Math.floor(Math.random() * charSets.numbers.length)];
                    break;
                case 'symbols':
                    replacementChar = charSets.symbols[Math.floor(Math.random() * charSets.symbols.length)];
                    break;
            }
            
            newPassword[randomIndex] = replacementChar;
        }
    });
    
    return newPassword.join('');
}

// Calculate password strength
function calculateStrength(password) {
    let score = 0;
    const length = password.length;
    
    // Length score
    if (length >= 8) score += 1;
    if (length >= 12) score += 1;
    if (length >= 16) score += 1;
    if (length >= 20) score += 1;
    
    // Character variety score
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^a-zA-Z0-9]/.test(password)) score += 1;
    
    // Deduct for repeated characters
    const uniqueChars = new Set(password).size;
    if (uniqueChars / length < 0.5) score -= 1;
    
    // Calculate entropy
    let charsetSize = 0;
    if (/[a-z]/.test(password)) charsetSize += 26;
    if (/[A-Z]/.test(password)) charsetSize += 26;
    if (/[0-9]/.test(password)) charsetSize += 10;
    if (/[^a-zA-Z0-9]/.test(password)) charsetSize += 8;
    
    const entropy = Math.log2(Math.pow(charsetSize, length));
    
    // Determine strength level
    let strength, label, percentage, crackTime;
    
    if (score <= 3) {
        strength = 'Weak';
        label = 'Weak';
        percentage = 33;
        crackTime = 'Seconds';
    } else if (score <= 6) {
        strength = 'Medium';
        label = 'Medium';
        percentage = 66;
        crackTime = 'Days';
    } else {
        strength = 'Strong';
        label = 'Strong';
        percentage = 100;
        crackTime = 'Centuries';
    }
    
    return {
        strength,
        label,
        percentage,
        entropy: entropy.toFixed(1),
        crackTime
    };
}

// Update strength meter
function updateStrengthMeter() {
    const password = passwordDisplay.textContent;
    if (password === 'Click Generate' || password === 'No character types selected') {
        return;
    }
    
    const strength = calculateStrength(password);
    
    strengthLabel.textContent = strength.label;
    strengthLabel.style.background = strength.strength === 'Weak' ? '#ff6b6b' :
                                   strength.strength === 'Medium' ? '#ffde59' : '#4ecdc4';
    
    meterFill.style.width = `${strength.percentage}%`;
    meterFill.style.background = strength.strength === 'Weak' ? 'linear-gradient(to right, #ff6b6b, #ff9e7d)' :
                               strength.strength === 'Medium' ? 'linear-gradient(to right, #ffde59, #ffb347)' :
                               'linear-gradient(to right, #4ecdc4, #44a08d)';
    
    entropyDisplay.textContent = `${strength.entropy} bits`;
    crackTimeDisplay.textContent = strength.crackTime;
}

// Generate and display password
function generateAndDisplay() {
    const password = generatePassword();
    passwordDisplay.textContent = password;
    updateStrengthMeter();
    showToast('New password generated!', 'success');
}

// Generate multiple passwords
function generateBatch() {
    const count = parseInt(batchCount.value) || 5;
    passwordList.innerHTML = '';
    
    for (let i = 0; i < count; i++) {
        const password = generatePassword();
        const strength = calculateStrength(password);
        
        const passwordItem = document.createElement('div');
        passwordItem.className = 'password-item';
        
        passwordItem.innerHTML = `
            <div class="pass-text">${password}</div>
            <div class="pass-strength strength-${strength.strength.toLowerCase()}">
                ${strength.strength}
            </div>
        `;
        
        // Add click to copy functionality
        passwordItem.addEventListener('click', () => {
            copyToClipboard(password);
            showToast('Password copied to clipboard!', 'success');
        });
        
        passwordList.appendChild(passwordItem);
    }
    
    showToast(`Generated ${count} passwords!`, 'success');
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Password copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        showToast('Failed to copy password', 'error');
    });
}

// Show toast notification
function showToast(message, type) {
    toastMessage.textContent = message;
    toast.className = 'toast';
    
    if (type === 'error') {
        toast.style.background = '#ff6b6b';
    } else if (type === 'success') {
        toast.style.background = '#4ecdc4';
    }
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Event Listeners
generateBtn.addEventListener('click', generateAndDisplay);
refreshBtn.addEventListener('click', generateAndDisplay);

copyBtn.addEventListener('click', () => {
    if (passwordDisplay.textContent !== 'Click Generate' && 
        passwordDisplay.textContent !== 'No character types selected') {
        copyToClipboard(passwordDisplay.textContent);
    }
});

batchGenerateBtn.addEventListener('click', generateBatch);

// Generate on page load
window.addEventListener('load', () => {
    generateAndDisplay();
    showToast('Welcome! Your password generator is ready.', 'success');
});

// Update strength meter on any change
[uppercaseCheck, lowercaseCheck, numbersCheck, symbolsCheck, customInput].forEach(element => {
    element.addEventListener('change', updateStrengthMeter);
});

// Add keyboard shortcut (Ctrl+G to generate)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'g') {
        e.preventDefault();
        generateAndDisplay();
    }
});
