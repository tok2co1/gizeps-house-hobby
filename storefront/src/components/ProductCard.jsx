"use client";
import React from 'react';
import { motion } from 'framer-motion';
import { Eye, ShoppingCart } from 'lucide-react';
import Link from 'next/link';

export default function ProductCard({ product }) {
    return (
        <motion.div
            className="product-card group flex flex-col"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
        >
            <Link href={`/product/${product.id}`} className="product-image-container group">
                {/* Product Image */}
                <img
                    src={product.image}
                    alt={product.title}
                    className="product-image"
                />

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center space-x-4">
                    <div className="bg-white p-3 rounded-full hover:bg-purple transition-colors duration-300 shadow-sm translate-y-4 group-hover:translate-y-0 transition-transform">
                        <Eye className="w-5 h-5 text-text-main hover:text-white" />
                    </div>
                    <div className="bg-white p-3 rounded-full hover:bg-purple transition-colors duration-300 shadow-sm translate-y-4 group-hover:translate-y-0 transition-transform delay-75">
                        <ShoppingCart className="w-5 h-5 text-text-main hover:text-white" />
                    </div>
                </div>

                {/* New Badge */}
                {product.isNew && (
                    <div className="absolute top-4 left-4 bg-primary text-black text-[10px] font-bold px-3 py-1 uppercase tracking-tighter">
                        YENİ
                    </div>
                )}
            </Link>

            {/* Product Info */}
            <div className="mt-6 flex flex-col items-center text-center">
                <span className="text-[10px] uppercase tracking-[0.2em] text-text-muted mb-2">
                    {product.category || "RUB ON TRANSFER"}
                </span>
                <Link href={`/product/${product.id}`}>
                    <h3 className="text-sm md:text-lg font-serif font-bold text-text-main group-hover:text-primary transition-colors duration-300 line-clamp-2 px-2 italic">
                        {product.title}
                    </h3>
                </Link>
                <div className="mt-3 flex flex-col items-center">
                    <span className="text-sm font-bold text-black tracking-tight">
                        {product.price} ₺
                    </span>
                    <span className="text-[10px] text-text-muted mt-1 uppercase tracking-widest">
                        STOK KODU: {product.sku}
                    </span>
                </div>
            </div>
        </motion.div>
    );
}

