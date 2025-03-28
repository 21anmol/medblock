// MedBlock Main JS
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Try to initialize auth if available
        if (typeof window.icpAuth !== 'undefined') {
            await window.icpAuth.initialize();
        }
    } catch (e) {
        console.log('Auth not fully initialized: ', e);
    }
    
    // Initialize theme
    initTheme();
    
    // Initialize animations
    initAnimation();
    
    // Initialize chatbot
    initChatbot();
    
    // Initialize navigation
    initNavigation();
    
    // Check for demo mode
    checkDemoMode();
    
    // Check authentication status
    checkAuthStatus();
    
    // Show demo mode indicator if in demo mode
    showDemoModeIndicator();
    
    // Initialize any cards or interactive elements
    initializeInteractiveElements();
});

function initTheme() {
    const themeToggle = document.getElementById('theme-toggle-checkbox');
    if (!themeToggle) return;
    
    const body = document.body;
    
    // Check localStorage for saved theme
    if(localStorage.getItem('theme') === 'light') {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeToggle.checked = true;
    }
    
    // Toggle theme on checkbox change
    themeToggle.addEventListener('change', function() {
        if(this.checked) {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        } else {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        }
    });
}

function initAnimation() {
    // Add animation to benefits section
    const benefitCards = document.querySelectorAll('.benefit-card');
    benefitCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });
    
    // Add animation to timeline items
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.3}s`;
    });
    
    // Testimonial slider
    const dots = document.querySelectorAll('.slider-dots .dot');
    const slides = document.querySelectorAll('.testimonial-slide');
    let currentSlide = 0;
    
    if (dots.length > 0 && slides.length > 0) {
        // Set up automatic slider
        setInterval(() => {
            slides[currentSlide].style.opacity = '0';
            dots[currentSlide].classList.remove('active');
            
            currentSlide = (currentSlide + 1) % slides.length;
            
            slides[currentSlide].style.opacity = '1';
            dots[currentSlide].classList.add('active');
        }, 5000);
        
        // Add click events to dots
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                slides[currentSlide].style.opacity = '0';
                dots[currentSlide].classList.remove('active');
                
                currentSlide = index;
                
                slides[currentSlide].style.opacity = '1';
                dots[currentSlide].classList.add('active');
            });
        });
    }
}

function initChatbot() {
    const chatbotButton = document.querySelector('.chatbot-button');
    const chatbotWidget = document.querySelector('.chatbot-widget');
    const closeChatbot = document.querySelector('.close-chatbot');
    const chatInput = document.querySelector('.chatbot-input input');
    const sendButton = document.querySelector('.chatbot-input button');
    const messagesContainer = document.querySelector('.chatbot-messages');
    
    // Toggle chatbot widget
    if (chatbotButton) {
        chatbotButton.addEventListener('click', function() {
            chatbotWidget.classList.toggle('active');
            if (chatInput) chatInput.focus();
        });
    }
    
    // Close chatbot
    if (closeChatbot) {
        closeChatbot.addEventListener('click', function() {
            chatbotWidget.classList.remove('active');
        });
    }
    
    // Send message
    function sendMessage() {
        if (!chatInput) return;
        
        const message = chatInput.value.trim();
        
        if (message) {
            // Add user message
            addMessage(message, 'user');
            
            // Clear input
            chatInput.value = '';
            
            // Get bot response (simulated)
            setTimeout(() => {
                getBotResponse(message);
            }, 800);
        }
    }
    
    // Add message to chat
    function addMessage(text, sender) {
        if (!messagesContainer) return;
        
        const messageElem = document.createElement('div');
        messageElem.className = `message ${sender}`;
        
        const contentElem = document.createElement('div');
        contentElem.className = 'message-content';
        contentElem.textContent = text;
        
        messageElem.appendChild(contentElem);
        messagesContainer.appendChild(messageElem);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Get bot response
    function getBotResponse(userMessage) {
        // Simulated responses
        const responses = [
            "I can help you understand your medical records and blockchain security.",
            "Your health data is securely stored on the blockchain and only accessible to authorized providers.",
            "You can view your complete medical history in the 'My Records' section.",
            "The AI diagnostics tools can help provide insights based on your health records.",
            "Would you like to know more about how MedBlock protects your health data?"
        ];
        
        const response = responses[Math.floor(Math.random() * responses.length)];
        addMessage(response, 'bot');
    }
    
    // Add event listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

function initNavigation() {
    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.dashboard-main');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
        });
    }
    
    // Add mobile navigation toggle if it doesn't exist
    if (!navToggle && sidebar && window.innerWidth < 992) {
        const toggle = document.createElement('button');
        toggle.className = 'nav-toggle';
        toggle.innerHTML = '<i class="fas fa-bars"></i>';
        document.body.appendChild(toggle);
        
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('expanded');
            document.body.classList.toggle('nav-open');
        });
    }
    
    // Add active class to current page nav item
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    
    navItems.forEach(item => {
        const link = item.querySelector('a');
        if (link) {
            const href = link.getAttribute('href');
            if (href === currentPage || (currentPage === '' && href === 'dashboard.html')) {
                item.classList.add('active');
            } else if (href && href !== '#' && currentPage.includes(href)) {
                item.classList.add('active');
            }
        }
    });
    
    // Add dropdown functionality to header user menu
    const userMenu = document.querySelector('.header-user');
    if (userMenu) {
        userMenu.addEventListener('click', () => {
            const dropdown = document.querySelector('.user-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('open');
            } else {
                // Create dropdown if it doesn't exist
                const newDropdown = document.createElement('div');
                newDropdown.className = 'user-dropdown';
                newDropdown.innerHTML = `
                    <ul>
                        <li><a href="#"><i class="fas fa-user"></i> My Profile</a></li>
                        <li><a href="#"><i class="fas fa-cog"></i> Settings</a></li>
                        <li><a href="#" class="logout-link"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
                    </ul>
                `;
                userMenu.appendChild(newDropdown);
                
                // Add event listener to logout link
                const logoutLink = newDropdown.querySelector('.logout-link');
                if (logoutLink) {
                    logoutLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        logout();
                    });
                }
                
                newDropdown.classList.add('open');
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userMenu.contains(e.target)) {
                const dropdown = document.querySelector('.user-dropdown');
                if (dropdown) {
                    dropdown.classList.remove('open');
                }
            }
        });
    }
}

function checkDemoMode() {
    // Check if in demo mode
    const isDemo = localStorage.getItem('demo_mode') === 'true';
    const isAuthenticated = localStorage.getItem('icp_authenticated') === 'true';
    
    const protectedPages = ['dashboard.html', 'blockchain.html', 'diagnostics.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    // Add demo badge if in demo mode
    if (isDemo) {
        // Only show if not already present
        if (!document.querySelector('.demo-indicator')) {
            const demoIndicator = document.createElement('div');
            demoIndicator.className = 'demo-indicator';
            demoIndicator.innerHTML = '<i class="fas fa-flask"></i> Demo Mode';
            document.body.appendChild(demoIndicator);
        }
        
        // Update user info in UI to demo user if available
        const userNameElements = document.querySelectorAll('.user-details h4, .header-user span');
        userNameElements.forEach(el => {
            el.innerText = 'Demo User';
        });
        
        // Change avatar if present
        const avatarElements = document.querySelectorAll('.user-avatar img, .header-user img');
        avatarElements.forEach(el => {
            el.src = 'https://randomuser.me/api/portraits/lego/1.jpg';
        });
    } else if (protectedPages.includes(currentPage) && !isAuthenticated) {
        // Not in demo mode and not authenticated on a protected page
        window.location.href = 'login.html?redirect=' + encodeURIComponent(currentPage);
    }
}

// Show notification function
function showNotification(title, message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        </div>
        <div class="notification-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
        <button class="close-notification">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Add close button functionality
    const closeButton = notification.querySelector('.close-notification');
    closeButton.addEventListener('click', function() {
        notification.classList.add('closing');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if(document.body.contains(notification)) {
            notification.classList.add('closing');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
    
    return notification;
}

// Make functions available globally for direct script usage
window.showNotification = showNotification;
window.checkDemoMode = checkDemoMode;

// Check if user is authenticated or in demo mode
function checkAuthStatus() {
    const isAuthenticated = localStorage.getItem('authenticated') === 'true';
    const demoMode = localStorage.getItem('demoMode') === 'true';
    const currentPage = window.location.pathname;
    
    // Check if current page requires authentication
    const protectedPages = [
        '/dashboard.html',
        '/blockchain.html',
        '/diagnostics.html',
        '/ai-diagnostics.html'
    ];
    
    const isProtectedPage = protectedPages.some(page => currentPage.endsWith(page));
    
    // If on a protected page and not authenticated or in demo mode, redirect to login
    if (isProtectedPage && !isAuthenticated && !demoMode) {
        // Store the page they were trying to access
        localStorage.setItem('redirectAfterLogin', currentPage);
        window.location.href = 'login.html';
        return false;
    }
    
    // Update UI based on authentication status
    updateUIForAuthStatus(isAuthenticated, demoMode);
    return true;
}

// Update UI elements based on authentication status
function updateUIForAuthStatus(isAuthenticated, demoMode) {
    // Update avatar if demo mode
    if (demoMode) {
        const avatarElements = document.querySelectorAll('.user-avatar img, .sidebar-profile img, .user-menu img');
        avatarElements.forEach(avatar => {
            avatar.src = 'https://randomuser.me/api/portraits/lego/1.jpg';
        });
    }
    
    // Update login/logout buttons
    const loginBtn = document.querySelector('.login-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    
    if (loginBtn) {
        loginBtn.style.display = isAuthenticated || demoMode ? 'none' : 'inline-flex';
    }
    
    if (logoutBtn) {
        logoutBtn.style.display = isAuthenticated || demoMode ? 'inline-flex' : 'none';
        logoutBtn.addEventListener('click', logout);
    }
}

// Logout function
function logout() {
    // Clear authentication status
    localStorage.removeItem('authenticated');
    localStorage.removeItem('demoMode');
    localStorage.removeItem('user');
    
    // Show notification
    showNotification('You have been logged out successfully', 'info');
    
    // Redirect to home page
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Show demo mode indicator
function showDemoModeIndicator() {
    const demoMode = localStorage.getItem('demoMode') === 'true';
    
    if (demoMode) {
        // If demo indicator doesn't exist yet, create it
        if (!document.querySelector('.demo-mode-indicator')) {
            const indicator = document.createElement('div');
            indicator.className = 'demo-mode-indicator';
            indicator.innerHTML = 'Demo Mode';
            document.body.appendChild(indicator);
        }
    }
}

// Initialize interactive elements like cards and charts
function initializeInteractiveElements() {
    // Initialize any charts if they exist
    initializeCharts();
    
    // Add interactive card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
    
    // Initialize ripple effect on buttons
    const buttons = document.querySelectorAll('.btn, .primary-button, .secondary-button');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
}

// Create ripple effect on buttons
function createRipple(event) {
    const button = event.currentTarget;
    
    // Remove any existing ripple
    const ripples = button.getElementsByClassName('ripple');
    Array.from(ripples).forEach(ripple => ripple.remove());
    
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');
    
    button.appendChild(circle);
}

// Initialize charts if they exist on the page
function initializeCharts() {
    // If Chart.js is loaded and charts exist
    if (typeof Chart !== 'undefined') {
        // Health Trends Chart
        const healthTrendCtx = document.getElementById('healthTrendsChart');
        if (healthTrendCtx) {
            new Chart(healthTrendCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Health Score',
                        data: [85, 82, 80, 87, 91, 93],
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: 50,
                            max: 100,
                            grid: {
                                color: 'rgba(160, 174, 192, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(160, 174, 192, 0.1)'
                            }
                        }
                    }
                }
            });
        }
    }
} 