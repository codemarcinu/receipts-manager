import React, { useState } from 'react';

const ReceiptVerificationForm = ({ initialData }) => {
    const [formData, setFormData] = useState({
        store: initialData.store || '',
        date: initialData.date || new Date().toISOString().split('T')[0],
        products: initialData.products.map(product => ({
            ...product,
            expiry_date: '',  // nowe pole
            notes: '',        // nowe pole
            current_quantity: product.quantity // początkowo taka sama jak quantity
        })) || [],
        total: initialData.total || 0
    });

    const handleProductChange = (index, field, value) => {
        const newProducts = [...formData.products];
        newProducts[index] = {
            ...newProducts[index],
            [field]: value
        };
        setFormData({
            ...formData,
            products: newProducts
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                window.location.href = '/receipts';
            } else {
                const error = await response.json();
                alert(`Błąd: ${error.message}`);
            }
        } catch (error) {
            alert('Wystąpił błąd podczas zapisywania danych');
        }
    };

    return (
        <div className="container mx-auto p-4">
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-bold mb-4">Weryfikacja paragonu</h2>

                    {/* Dane podstawowe */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Sklep</label>
                            <input
                                type="text"
                                value={formData.store}
                                onChange={(e) => setFormData({...formData, store: e.target.value})}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Data</label>
                            <input
                                type="date"
                                value={formData.date}
                                onChange={(e) => setFormData({...formData, date: e.target.value})}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                required
                            />
                        </div>
                    </div>

                    {/* Lista produktów */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-medium">Produkty</h3>
                        {formData.products.map((product, index) => (
                            <div key={index} className="bg-gray-50 p-4 rounded-lg">
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Nazwa</label>
                                        <input
                                            type="text"
                                            value={product.name}
                                            onChange={(e) => handleProductChange(index, 'name', e.target.value)}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Ilość</label>
                                        <input
                                            type="number"
                                            step="0.001"
                                            value={product.quantity}
                                            onChange={(e) => handleProductChange(index, 'quantity', parseFloat(e.target.value))}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Jednostka</label>
                                        <select
                                            value={product.unit}
                                            onChange={(e) => handleProductChange(index, 'unit', e.target.value)}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                            required
                                        >
                                            <option value="szt">szt</option>
                                            <option value="kg">kg</option>
                                            <option value="g">g</option>
                                            <option value="l">l</option>
                                            <option value="ml">ml</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Cena</label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={product.price}
                                            onChange={(e) => handleProductChange(index, 'price', parseFloat(e.target.value))}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Data ważności</label>
                                        <input
                                            type="date"
                                            value={product.expiry_date}
                                            onChange={(e) => handleProductChange(index, 'expiry_date', e.target.value)}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                        />
                                    </div>
                                    <div className="col-span-2">
                                        <label className="block text-sm font-medium text-gray-700">Notatki</label>
                                        <textarea
                                            value={product.notes}
                                            onChange={(e) => handleProductChange(index, 'notes', e.target.value)}
                                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                            rows="2"
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Suma */}
                    <div className="mt-6">
                        <label className="block text-sm font-medium text-gray-700">Suma</label>
                        <input
                            type="number"
                            step="0.01"
                            value={formData.total}
                            onChange={(e) => setFormData({...formData, total: parseFloat(e.target.value)})}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                            required
                        />
                    </div>

                    {/* Przyciski */}
                    <div className="mt-6 flex justify-end space-x-3">
                        <button
                            type="button"
                            onClick={() => window.location.href = '/receipts'}
                            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                            Anuluj
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        >
                            Zapisz
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default ReceiptVerificationForm;