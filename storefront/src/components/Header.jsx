"use client";
import React from 'react';
import Link from 'next/link';
import { ShoppingBag, Search, User, Menu } from 'lucide-react';

export default function Header() {
    return (
        <header className="w-full flex flex-col border-b border-gray-100">
            {/* Top Promo Bar */}
            <div className="promo-bar bg-purple px-4 py-2 text-xs md:text-sm font-semibold text-white uppercase tracking-widest">
                1000 TL Üzeri Ücretsiz Kargo • Gizep's Hobby House
            </div>

            {/* Main Header */}
            <div className="container mx-auto px-4 md:px-8 py-6 flex items-center justify-between">
                {/* Mobile Menu Icon */}
                <div className="md:hidden">
                    <Menu className="w-6 h-6 text-text-main" />
                </div>

                {/* Search Icon (Left on Desktop) */}
                <div className="hidden md:flex items-center space-x-4 w-1/3">
                    <Search className="w-5 h-5 text-text-muted cursor-pointer hover:text-primary transition-colors" />
                </div>

                {/* Centered Logo */}
                <div className="flex-1 flex justify-center w-1/3">
                    <Link href="/" className="flex flex-col items-center group">
                        <span className="text-3xl md:text-5xl font-pacifico text-purple transition-transform duration-300 group-hover:scale-105">
                            Gizep's Hobby House
                        </span>
                    </Link>
                </div>

                {/* Icons (Right) */}
                <div className="flex items-center justify-end space-x-6 w-1/3">
                    <div className="hidden md:flex items-center cursor-pointer group">
                        <User className="w-5 h-5 text-text-muted group-hover:text-primary transition-colors" />
                        <span className="ml-2 text-xs font-medium text-text-muted group-hover:text-primary hidden lg:inline">HESABIM</span>
                    </div>
                    <div className="relative cursor-pointer group">
                        <ShoppingBag className="w-5 h-5 text-text-muted group-hover:text-primary transition-colors" />
                        <span className="absolute -top-2 -right-2 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">
                            0
                        </span>
                    </div>
                </div>
            </div>

            {/* Navigation (Desktop) */}
            <nav className="hidden md:flex items-center justify-center space-x-8 py-4 text-xs font-semibold tracking-widest text-text-main uppercase">
                <Link href="/" className="hover:text-primary transition-colors border-b-2 border-primary">ANA SAYFA</Link>
                <Link href="#" className="hover:text-primary transition-colors border-b-2 border-transparent">YENİ GELENLER</Link>
                <Link href="#" className="hover:text-primary transition-colors border-b-2 border-transparent">RUBON TRANSFER</Link>
                <Link href="#" className="hover:text-primary transition-colors border-b-2 border-transparent">ATÖLYE</Link>
                <Link href="#" className="hover:text-primary transition-colors border-b-2 border-transparent">İLETİŞİM</Link>
            </nav>
        </header>
    );
}
