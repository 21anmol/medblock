// MedBlock Authentication Module (ICP Internet Identity Integration)

// Create a global reference to the auth functionality
window.icpAuth = {
    // Check if the user is authenticated
    isAuthenticated: function() {
        return localStorage.getItem('authenticated') === 'true';
    },
    
    // Initialize authentication
    initialize: async function() {
        console.log('Initializing MedBlock authentication...');
        
        // Check if we have the identity in local storage
        if (this.isAuthenticated()) {
            console.log('User is already authenticated');
            this.updateUI(true);
            return true;
        }
        
        // Add event listener to the login form if it exists
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', this.handleLogin.bind(this));
        }
        
        return false;
    },
    
    // Handle login form submission
    handleLogin: function(event) {
        event.preventDefault();
        console.log('Processing login...');
        
        // In a real implementation, this would connect to ICP Authentication
        // This is a simplified version for demonstration
        this.simulateIcpAuth()
            .then(principal => {
                if (principal) {
                    // Store authentication state
                    localStorage.setItem('authenticated', 'true');
                    localStorage.setItem('principal', principal);
                    
                    // Show success notification
                    this.showNotification('Authentication Successful', 'You have been securely logged in using Internet Identity', 'success');
                    
                    // Update UI
                    this.updateUI(true);
                    
                    // Redirect after delay
                    setTimeout(() => {
                        // Check if there's a redirect URL stored
                        const redirect = localStorage.getItem('redirectAfterLogin');
                        if (redirect) {
                            localStorage.removeItem('redirectAfterLogin');
                            window.location.href = redirect;
                        } else {
                            window.location.href = 'dashboard.html';
                        }
                    }, 1500);
                } else {
                    // Show error
                    const errorElement = document.getElementById('login-error');
                    if (errorElement) {
                        errorElement.textContent = 'Authentication failed. Please try again.';
                        errorElement.style.display = 'block';
                    }
                }
            })
            .catch(error => {
                console.error('Authentication error:', error);
                const errorElement = document.getElementById('login-error');
                if (errorElement) {
                    errorElement.textContent = 'Authentication error: ' + error.message;
                    errorElement.style.display = 'block';
                }
            });
    },
    
    // Simulate ICP Authentication
    simulateIcpAuth: function() {
        return new Promise((resolve) => {
            // Simulate authentication delay
            setTimeout(() => {
                // Generate a fake principal ID
                const principalId = 'w4gpt-xutji-' + Math.random().toString(36).substring(2, 10);
                resolve(principalId);
            }, 1000);
        });
    },
    
    // Handle logout
    logout: function() {
        console.log('Logging out...');
        
        // Clear authentication state
        localStorage.removeItem('authenticated');
        localStorage.removeItem('principal');
        
        // Show logout notification
        this.showNotification('Logged Out', 'You have been securely logged out', 'info');
        
        // Update UI
        this.updateUI(false);
        
        // Redirect to home after delay
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    },
    
    // Update UI based on authentication state
    updateUI: function(isAuthenticated) {
        // Update login/logout buttons
        const loginButtons = document.querySelectorAll('.login-btn, .login-button');
        const logoutButtons = document.querySelectorAll('.logout-btn');
        
        loginButtons.forEach(btn => {
            if (btn) btn.style.display = isAuthenticated ? 'none' : 'inline-flex';
        });
        
        logoutButtons.forEach(btn => {
            if (btn) {
                btn.style.display = isAuthenticated ? 'inline-flex' : 'none';
                
                // Add logout event listener
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.logout();
                });
            }
        });
        
        // Update user sections if they exist
        const userSections = document.querySelectorAll('.user-info, .user-section, .header-user');
        userSections.forEach(section => {
            if (section) section.style.display = isAuthenticated ? 'flex' : 'none';
        });
    },
    
    // Show notification
    showNotification: function(title, message, type = 'info') {
        // Check if we have the global notification function
        if (typeof window.showNotification === 'function') {
            window.showNotification(title, message, type);
            return;
        }
        
        // Fallback implementation
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
        
        document.body.appendChild(notification);
        
        const closeButton = notification.querySelector('.close-notification');
        closeButton.addEventListener('click', function() {
            notification.classList.add('closing');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
        
        setTimeout(() => {
            notification.classList.add('closing');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }
};

// Use event listener to track when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize auth system
    window.icpAuth.initialize().catch(console.error);
    
    // Setup demo login functionality if that button exists
    const demoLoginBtn = document.getElementById('demo-login');
    if (demoLoginBtn) {
        demoLoginBtn.addEventListener('click', function() {
            console.log('Demo login clicked');
            // Set demo mode flag in localStorage
            localStorage.setItem('demoMode', 'true');
            
            // Show success notification
            window.icpAuth.showNotification('Demo Mode Activated', 'You are now using MedBlock in demo mode', 'success');
            
            // Redirect to dashboard after a short delay
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        });
    }
}); 