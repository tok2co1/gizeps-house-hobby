"use client";
import React from 'react';
import ProductCard from './ProductCard';

export default function ProductGrid({ products, categories, selectedCategory, onCategoryChange }) {
    return (
        <section className="container mx-auto px-4 md:px-8 py-16">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 space-y-4 md:space-y-0">
                <div>
                    <h2 className="text-2xl md:text-4xl font-serif font-bold text-black tracking-tight uppercase">
                        RUB ON TRANSFER <span className="text-primary font-normal text-xl ml-2 tracking-widest italic">KOLEKSİYONU</span>
                    </h2>
                    <div className="w-24 h-1 bg-primary mt-4"></div>
                </div>

                <div className="flex items-center flex-wrap gap-4 text-[11px] font-bold tracking-widest text-text-muted uppercase">
                    {categories && categories.map((cat) => (
                        <button
                            key={cat}
                            onClick={() => onCategoryChange(cat)}
                            className={`hover:text-primary transition-colors pb-1 ${selectedCategory === cat ? 'text-primary border-b border-primary' : ''}`}
                        >
                            {cat}
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-12">
                {products.map((product) => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </section>
    );
}
