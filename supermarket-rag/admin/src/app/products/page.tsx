'use client';

import { useState, useEffect } from 'react';
import { Search, Plus, Edit2, Check, X, Eye, EyeOff, Loader2 } from 'lucide-react';

interface Product {
    id: number;
    text: string;
    metadata_: any;
    is_enabled: boolean;
    updated_at: string;
}

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [isAdding, setIsAdding] = useState(false);
    const [newProduct, setNewProduct] = useState({ text: '', shop_name: 'Coles' });
    const [editingId, setEditingId] = useState<number | null>(null);
    const [editText, setEditText] = useState('');

    useEffect(() => {
        fetchProducts();
    }, []);

    const fetchProducts = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/admin/products');
            const data = await res.json();
            if (Array.isArray(data)) {
                setProducts(data);
            } else {
                console.error('API Error:', data);
                setProducts([]);
            }
        } catch (e) {
            console.error(e);
            setProducts([]);
        } finally {
            setLoading(false);
        }
    };

    const handleToggleVisibility = async (id: number, currentStatus: boolean) => {
        try {
            const res = await fetch(`/api/admin/products/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_enabled: !currentStatus })
            });
            if (res.ok) {
                setProducts(products.map(p => p.id === id ? { ...p, is_enabled: !currentStatus } : p));
            }
        } catch (e) {
            console.error(e);
        }
    };

    const handleSaveEdit = async (id: number) => {
        try {
            const res = await fetch(`/api/admin/products/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: editText })
            });
            if (res.ok) {
                setProducts(products.map(p => p.id === id ? { ...p, text: editText } : p));
                setEditingId(null);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const handleAddProduct = async () => {
        try {
            const res = await fetch('/api/admin/products', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newProduct)
            });
            if (res.ok) {
                setIsAdding(false);
                setNewProduct({ text: '', shop_name: 'Coles' });
                fetchProducts();
            }
        } catch (e) {
            console.error(e);
        }
    };

    const filteredProducts = products.filter(p =>
        p.text.toLowerCase().includes(search.toLowerCase()) ||
        p.metadata_?.shop_name?.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="animate-fade-in">
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <div>
                    <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>Products</h1>
                    <p style={{ color: 'var(--muted-foreground)' }}>Manage RAG indexing and manually add product entries.</p>
                </div>
                <button className="btn btn-primary" onClick={() => setIsAdding(true)} style={{ gap: '0.5rem' }}>
                    <Plus size={18} /> Add Product
                </button>
            </header>

            {isAdding && (
                <div className="card" style={{ marginBottom: '2rem', animation: 'fadeIn 0.3s ease' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>Add New Product Entry</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Product Text / Content</label>
                            <textarea
                                className="card"
                                style={{ width: '100%', minHeight: '100px', background: 'var(--background)', padding: '1rem' }}
                                value={newProduct.text}
                                onChange={(e) => setNewProduct({ ...newProduct, text: e.target.value })}
                                placeholder="e.g. Coles Milk 2L - $3.50, SAVE $0.50"
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Supermarket</label>
                            <select
                                className="card"
                                style={{ width: '100%', background: 'var(--background)', padding: '0.75rem' }}
                                value={newProduct.shop_name}
                                onChange={(e) => setNewProduct({ ...newProduct, shop_name: e.target.value })}
                            >
                                <option value="Coles">Coles</option>
                                <option value="Woolworths">Woolworths</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                            <button className="btn btn-primary" onClick={handleAddProduct}>Save Product</button>
                            <button className="btn btn-secondary" onClick={() => setIsAdding(false)}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            <div style={{ position: 'relative', marginBottom: '2rem' }}>
                <Search style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted-foreground)' }} size={18} />
                <input
                    type="text"
                    placeholder="Search products or shops..."
                    className="card"
                    style={{ width: '100%', paddingLeft: '3rem', background: 'var(--secondary)' }}
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border)' }}>
                        <tr>
                            <th style={{ textAlign: 'left', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>ID</th>
                            <th style={{ textAlign: 'left', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>Image</th>
                            <th style={{ textAlign: 'left', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>Content</th>
                            <th style={{ textAlign: 'left', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>Shop</th>
                            <th style={{ textAlign: 'left', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>Status</th>
                            <th style={{ textAlign: 'right', padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: 600 }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan={6} style={{ padding: '3rem', textAlign: 'center' }}>
                                    <Loader2 className="animate-spin" style={{ margin: '0 auto' }} />
                                </td>
                            </tr>
                        ) : filteredProducts.length === 0 ? (
                            <tr>
                                <td colSpan={6} style={{ padding: '3rem', textAlign: 'center', color: 'var(--muted-foreground)' }}>No products found</td>
                            </tr>
                        ) : filteredProducts.map((p) => (
                            <tr key={p.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem' }}>{p.id}</td>
                                <td style={{ padding: '1rem 1.5rem' }}>
                                    {p.metadata_?.page_thumbnail_url ? (
                                        <a
                                            href={p.metadata_.page_image_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="product-image-preview"
                                        >
                                            <img
                                                src={p.metadata_.page_thumbnail_url}
                                                alt="Catalog page"
                                                style={{
                                                    width: '40px',
                                                    height: '40px',
                                                    borderRadius: '4px',
                                                    objectFit: 'cover',
                                                    border: '1px solid var(--border)',
                                                    transition: 'transform 0.2s',
                                                    cursor: 'zoom-in'
                                                }}
                                                onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.1)')}
                                                onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                                            />
                                        </a>
                                    ) : (
                                        <div style={{
                                            width: '40px',
                                            height: '40px',
                                            borderRadius: '4px',
                                            background: 'var(--secondary)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            fontSize: '0.6rem',
                                            color: 'var(--muted-foreground)',
                                            border: '1px solid var(--border)'
                                        }}>
                                            No Img
                                        </div>
                                    )}
                                </td>
                                <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem' }}>
                                    {editingId === p.id ? (
                                        <input
                                            type="text"
                                            className="card"
                                            style={{ padding: '0.5rem', width: '100%', background: 'var(--background)' }}
                                            value={editText}
                                            onChange={(e) => setEditText(e.target.value)}
                                            autoFocus
                                        />
                                    ) : (
                                        <div style={{ maxWidth: '400px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {p.text}
                                        </div>
                                    )}
                                </td>
                                <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem' }}>
                                    <span style={{ padding: '0.25rem 0.5rem', borderRadius: '4px', background: 'var(--background)', fontSize: '0.75rem' }}>
                                        {p.metadata_?.shop_name || 'N/A'}
                                    </span>
                                </td>
                                <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem' }}>
                                    <span style={{ color: p.is_enabled ? '#10b981' : '#f43f5e' }}>
                                        {p.is_enabled ? 'Active' : 'Disabled'}
                                    </span>
                                </td>
                                <td style={{ padding: '1rem 1.5rem', textAlign: 'right' }}>
                                    <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                                        {editingId === p.id ? (
                                            <>
                                                <button className="btn btn-primary" onClick={() => handleSaveEdit(p.id)} style={{ padding: '0.4rem' }}>
                                                    <Check size={16} />
                                                </button>
                                                <button className="btn btn-secondary" onClick={() => setEditingId(null)} style={{ padding: '0.4rem' }}>
                                                    <X size={16} />
                                                </button>
                                            </>
                                        ) : (
                                            <>
                                                <button className="btn btn-secondary" onClick={() => { setEditingId(p.id); setEditText(p.text); }} style={{ padding: '0.4rem' }}>
                                                    <Edit2 size={16} />
                                                </button>
                                                <button className="btn btn-secondary" onClick={() => handleToggleVisibility(p.id, p.is_enabled)} style={{ padding: '0.4rem' }}>
                                                    {p.is_enabled ? <Eye size={16} /> : <EyeOff size={16} />}
                                                </button>
                                            </>
                                        )}
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
