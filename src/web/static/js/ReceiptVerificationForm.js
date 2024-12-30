/**
 * ReceiptVerificationForm.js
 * Obsługa formularza weryfikacji paragonów
 */

class ReceiptVerificationForm {
    constructor() {
        this.form = document.getElementById('verifyForm');
        if (!this.form) {
            console.warn('Element #verifyForm nie został znaleziony w DOM.');
            return;
        }
        this.productsContainer = document.getElementById('products-container');
        this.totalInput = document.getElementById('total_amount');

        this.initializeEventListeners();
        this.initializeExistingProducts();
    }

    initializeEventListeners() {
        let debounceTimeout;
        this.form.addEventListener('input', (e) => {
            if (e.target.classList.contains('price-input') ||
                e.target.classList.contains('quantity-input')) {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(() => this.updateTotalAmount(), 300);
            }
        });

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    initializeExistingProducts() {
        document.querySelectorAll('.product-name').forEach(input => {
            this.initializeAutocomplete(input);
        });

        this.updateTotalAmount();
    }

    async initializeAutocomplete(input) {
        let timeout = null;
        
        input.addEventListener('input', async (e) => {
            clearTimeout(timeout);
            const query = e.target.value;
            
            if (query.length < 2) return;
            
            timeout = setTimeout(async () => {
                try {
                    const response = await fetch(`/receipts/api/products/suggestions?query=${encodeURIComponent(query)}`);
                    if (!response.ok) throw new Error('Network response was not ok');
                    
                    const suggestions = await response.json();
                    if (suggestions.length > 0) {
                        const productItem = input.closest('.product-item');
                        this.fillProductDetails(productItem, suggestions[0]);
                    }
                } catch (error) {
                    console.error('Błąd podczas pobierania sugestii:', error);
                    this.showNotification('error', 'Nie udało się pobrać sugestii produktów');
                }
            }, 300);
        });
    }

    fillProductDetails(productItem, suggestion) {
        const unitInput = productItem.querySelector('[name$="unit"]');
        const categorySelect = productItem.querySelector('[name$="category_id"]');
        
        if (unitInput) unitInput.value = suggestion.unit || '';
        if (categorySelect) categorySelect.value = suggestion.category_id || '0';
    }

    addProduct() {
        const template = document.getElementById('product-template');
        const productsCount = document.querySelectorAll('.product-item').length;
        
        const newProduct = template.content.cloneNode(true);
        
        const fields = newProduct.querySelectorAll('input, select');
        fields.forEach(field => {
            const name = field.getAttribute('name');
            if (name) {
                field.setAttribute('name', name.replace(/\d+/, productsCount.toString()));
            }
        });
        
        this.productsContainer.appendChild(newProduct);
        
        const nameInput = this.productsContainer.lastElementChild.querySelector('.product-name');
        if (nameInput) {
            this.initializeAutocomplete(nameInput);
        }
        
        this.updateTotalAmount();
    }

    removeProduct(button) {
        const productItem = button.closest('.product-item');
        
        productItem.style.opacity = '0';
        setTimeout(() => {
            productItem.remove();
            this.updateTotalAmount();
        }, 300);
    }

    updateTotalAmount() {
        const products = document.querySelectorAll('.product-item');
        let total = 0;
        
        products.forEach(product => {
            const price = parseFloat(product.querySelector('.price-input')?.value) || 0;
            const quantity = parseFloat(product.querySelector('.quantity-input')?.value) || 0;
            total += price * quantity;
        });
        
        if (this.totalInput) {
            this.totalInput.value = total.toFixed(2);
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: new FormData(this.form)
            });

            const data = await response.json();
            
            if (response.ok) {
                this.showNotification('success', 'Paragon został pomyślnie zapisany');
                setTimeout(() => {
                    window.location.href = '/receipts/list';
                }, 1500);
            } else {
                this.showNotification('error', data.message || 'Wystąpił błąd podczas zapisywania paragonu');
            }
        } catch (error) {
            console.error('Błąd podczas zapisywania:', error);
            this.showNotification('error', 'Wystąpił błąd podczas zapisywania paragonu');
        }
    }

    showNotification(type, message) {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `md-alert md-alert-${type} animate-bounce-in`;
        notification.textContent = message;

        container.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('animate-fade-out');
            notification.addEventListener('animationend', () => notification.remove(), { once: true });
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const formElement = document.getElementById('verifyForm');
    if (!formElement) {
        console.warn('Element #verifyForm nie istnieje. Sprawdź HTML i upewnij się, że formularz został załadowany.');
        return;
    }
    window.receiptForm = new ReceiptVerificationForm();
});

window.addProduct = () => window.receiptForm?.addProduct();
window.removeProduct = (button) => window.receiptForm?.removeProduct(button);
