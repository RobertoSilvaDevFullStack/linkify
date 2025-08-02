// =============================================================================
// LINKIFY - MAIN JAVASCRIPT
// =============================================================================

// Global variables
let currentUser = null;
let userLinks = [];

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Make authenticated API request
 */
async function authenticatedFetch(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };
    
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(url, config);
    
    // If unauthorized, redirect to login
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        return;
    }
    
    return response;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type} slide-in`;
    
    const icon = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle'
    };
    
    const color = {
        success: 'text-green-600',
        error: 'text-red-600',
        info: 'text-blue-600',
        warning: 'text-yellow-600'
    };
    
    toast.innerHTML = `
        <div class="flex items-center">
            <i class="${icon[type]} ${color[type]} mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-gray-400 hover:text-gray-600">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, duration);
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('URL copiada para a área de transferência!', 'success');
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('URL copiada para a área de transferência!', 'success');
    }
}

/**
 * Format date to Brazilian format
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

/**
 * Format date with time
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Check if date is expired
 */
function isExpired(dateString) {
    return new Date() > new Date(dateString);
}

/**
 * Check if date is expiring soon (within 7 days)
 */
function isExpiringSoon(dateString) {
    const now = new Date();
    const expiry = new Date(dateString);
    const diffTime = expiry - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7 && diffDays > 0;
}

/**
 * Validate URL format
 */
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

/**
 * Normalize URL (add https if missing)
 */
function normalizeUrl(url) {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        return 'https://' + url;
    }
    return url;
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

/**
 * User authentication functions
 */
const Auth = {
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            return { success: true, data };
        }
        
        return { success: false, error: data.detail || 'Erro ao fazer login' };
    },
    
    async register(username, email, password) {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            return { success: true, data };
        }
        
        return { success: false, error: data.detail || data.message || 'Erro ao criar conta' };
    },
    
    async getCurrentUser() {
        const response = await authenticatedFetch('/api/auth/me');
        if (response && response.ok) {
            const user = await response.json();
            currentUser = user;
            return user;
        }
        throw new Error('Failed to get current user');
    },
    
    logout() {
        localStorage.removeItem('access_token');
        currentUser = null;
        window.location.href = '/';
    }
};

/**
 * Link management functions
 */
const Links = {
    async create(originalUrl) {
        const response = await authenticatedFetch('/api/shorten', {
            method: 'POST',
            body: JSON.stringify({
                original_url: normalizeUrl(originalUrl)
            })
        });
        
        const data = await response.json();
        
        if (response && response.ok && data.success) {
            return { success: true, data };
        }
        
        return { success: false, error: data.message || 'Erro ao criar link' };
    },
    
    async getUserLinks() {
        const response = await authenticatedFetch('/api/user/links');
        if (response && response.ok) {
            const data = await response.json();
            userLinks = data.links || [];
            return data.links || [];
        }
        throw new Error('Failed to get user links');
    },
    
    async delete(linkId) {
        const response = await authenticatedFetch(`/api/user/links/${linkId}`, {
            method: 'DELETE'
        });
        
        if (response && response.ok) {
            const data = await response.json();
            return { success: true, data };
        }
        
        return { success: false, error: 'Erro ao excluir link' };
    },
    
    async getStats() {
        const response = await authenticatedFetch('/api/user/stats');
        if (response && response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get stats');
    }
};

// =============================================================================
// DOM MANIPULATION FUNCTIONS
// =============================================================================

/**
 * Loading state management
 */
function setLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Carregando...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || button.innerHTML;
    }
}

/**
 * Form validation
 */
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        const value = input.value.trim();
        
        if (!value) {
            input.classList.add('error-border');
            isValid = false;
        } else {
            input.classList.remove('error-border');
            
            // Specific validations
            if (input.type === 'email' && !input.validity.valid) {
                input.classList.add('error-border');
                isValid = false;
            }
            
            if (input.type === 'url' && !isValidUrl(normalizeUrl(value))) {
                input.classList.add('error-border');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

// =============================================================================
// EVENT LISTENERS
// =============================================================================

// Global click handler for copy buttons
document.addEventListener('click', function(e) {
    if (e.target.matches('.copy-btn') || e.target.closest('.copy-btn')) {
        const button = e.target.closest('.copy-btn') || e.target;
        const text = button.dataset.text || button.previousElementSibling?.value;
        if (text) {
            copyToClipboard(text);
        }
    }
});

// Global form validation
document.addEventListener('input', function(e) {
    if (e.target.matches('input[required]')) {
        e.target.classList.remove('error-border');
    }
});

// =============================================================================
// INITIALIZATION
// =============================================================================

// Page-specific initialization
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    const main = document.querySelector('main');
    if (main) {
        main.classList.add('fade-in');
    }
    
    // Initialize any tooltips or other components
    // This can be expanded based on needs
});

// Export functions for global use
window.Linkify = {
    Auth,
    Links,
    showToast,
    copyToClipboard,
    formatDate,
    formatDateTime,
    isExpired,
    isExpiringSoon,
    isValidUrl,
    normalizeUrl,
    setLoading,
    validateForm
};
