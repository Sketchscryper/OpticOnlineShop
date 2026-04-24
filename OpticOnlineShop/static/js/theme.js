// Получение текущей темы из localStorage
function getCurrentTheme() {
    let theme = localStorage.getItem('theme');
    if (!theme) {
        theme = 'light';
        localStorage.setItem('theme', theme);
    }
    return theme;
}

// Применение темы
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.checked = theme === 'dark';
    }
    
    updateThemeUI(theme);
}

// Обновление интерфейса темы
function updateThemeUI(theme) {
    const lightText = document.getElementById('theme-text-light');
    const darkText = document.getElementById('theme-text-dark');
    
    if (theme === 'light') {
        if (lightText) {
            lightText.style.fontWeight = 'bold';
            lightText.style.opacity = '1';
        }
        if (darkText) {
            darkText.style.fontWeight = 'normal';
            darkText.style.opacity = '0.6';
        }
    } else {
        if (darkText) {
            darkText.style.fontWeight = 'bold';
            darkText.style.opacity = '1';
        }
        if (lightText) {
            lightText.style.fontWeight = 'normal';
            lightText.style.opacity = '0.6';
        }
    }
}

// Переключение темы
function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    const theme = getCurrentTheme();
    setTheme(theme);
    
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', toggleTheme);
    }
});