// Oyun durumu
let balance = 1000;
let currentBet = 0;
let selectedNumber = null;
let isSpinning = false;

// Renk tanımlamaları
const colors = {
    0: 'green',
    1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red',
    6: 'black', 7: 'red', 8: 'black', 9: 'red', 10: 'black',
    11: 'black', 12: 'red', 13: 'black', 14: 'red', 15: 'black',
    16: 'red', 17: 'black', 18: 'red', 19: 'red', 20: 'black',
    21: 'red', 22: 'black', 23: 'red', 24: 'black', 25: 'red',
    26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red',
    31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black',
    36: 'red'
};

// Sayı gridini oluştur
function createNumberGrid() {
    const grid = document.querySelector('.numbers-grid');
    for (let i = 0; i <= 36; i++) {
        const button = document.createElement('button');
        button.className = `bet-button number ${colors[i]}`;
        button.textContent = i;
        button.dataset.number = i;
        button.addEventListener('click', () => selectNumber(i));
        grid.appendChild(button);
    }
}

// Sayı seçme
function selectNumber(number) {
    if (isSpinning) return;
    selectedNumber = number;
    updateUI();
}

// Bahis yapma
function placeBet() {
    const betAmount = parseInt(document.getElementById('bet-input').value);
    if (betAmount > balance || selectedNumber === null) return;
    
    currentBet = betAmount;
    balance -= betAmount;
    updateUI();
}

// Çarkı çevir
function spinWheel() {
    if (isSpinning || currentBet === 0) return;
    
    isSpinning = true;
    const ball = document.querySelector('.ball');
    const wheel = document.querySelector('.wheel-inner');
    
    // Rastgele sayı seç
    const winningNumber = Math.floor(Math.random() * 37);
    
    // Animasyon
    wheel.style.transition = 'transform 5s cubic-bezier(0.17, 0.67, 0.83, 0.67)';
    wheel.style.transform = `rotate(${3600 + winningNumber * (360/37)}deg)`;
    
    setTimeout(() => {
        checkWin(winningNumber);
        isSpinning = false;
        currentBet = 0;
        selectedNumber = null;
        updateUI();
    }, 5000);
}

// Kazanç kontrolü
function checkWin(winningNumber) {
    if (selectedNumber === winningNumber) {
        balance += currentBet * 36;
        alert(`Tebrikler! ${winningNumber} numarasına düştü ve ${currentBet * 36}₺ kazandınız!`);
    } else {
        alert(`Maalesef, ${winningNumber} numarasına düştü. Kaybettiniz.`);
    }
}

// UI güncelleme
function updateUI() {
    document.getElementById('balance').textContent = balance;
    document.getElementById('current-bet').textContent = currentBet;
    
    // Seçili sayıyı vurgula
    document.querySelectorAll('.number').forEach(button => {
        button.classList.remove('selected');
        if (parseInt(button.dataset.number) === selectedNumber) {
            button.classList.add('selected');
        }
    });
}

// Event listeners
document.getElementById('place-bet').addEventListener('click', placeBet);
document.getElementById('spin-button').addEventListener('click', spinWheel);

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', () => {
    createNumberGrid();
    updateUI();
}); 