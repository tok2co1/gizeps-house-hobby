"use client";
import React from 'react';
import Link from 'next/link';
import { ShoppingBag, Search, User, Menu } from 'lucide-react';

import { useDealer } from '../context/DealerContext';

export default function Header() {
    const { isDealer, login, logout, isLoginOpen, setIsLoginOpen } = useDealer();
    const [password, setPassword] = React.useState('');
    const [error, setError] = React.useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        if (login(password)) {
            setPassword('');
            setError('');
        } else {
            setError('Hatalı şifre!');
        }
    };

    return (
        <header className="w-full flex flex-col border-b border-gray-100 relative z-50">
            {/* Top Promo Bar */}
            <div className="promo-bar bg-purple px-4 py-2 text-xs md:text-sm font-semibold text-white uppercase tracking-widest flex justify-center relative">
                <span>1000 TL Üzeri Ücretsiz Kargo • Gizep's Hobby House</span>
                {isDealer && (
                    <span className="absolute right-4 bg-white text-purple px-2 py-0.5 rounded text-[10px] font-bold animate-pulse">
                        BAYİ MODU AKTİF
                    </span>
                )}
            </div>

            {/* Login Modal */}
            {isLoginOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[100]">
                    <div className="bg-white p-8 rounded-lg shadow-xl w-80 relative">
                        <button
                            onClick={() => setIsLoginOpen(false)}
                            className="absolute top-2 right-2 text-gray-400 hover:text-black"
                        >
                            ✕
                        </button>
                        <h2 className="text-xl font-pacifico text-purple mb-4 text-center">Bayi Girişi</h2>
                        <form onSubmit={handleLogin} className="flex flex-col space-y-4">
                            <input
                                type="password"
                                placeholder="Bayi Şifresi"
                                className="border p-2 rounded focus:outline-none focus:border-purple text-black"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            {error && <p className="text-red-500 text-xs">{error}</p>}
                            <button type="submit" className="bg-purple text-white py-2 rounded hover:bg-purple-700 transition">
                                GİRİŞ YAP
                            </button>
                        </form>
                    </div>
                </div>
            )}

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
                    <div
                        className="hidden md:flex items-center cursor-pointer group"
                        onClick={() => isDealer ? logout() : setIsLoginOpen(true)}
                    >
                        <User className={`w-5 h-5 transition-colors ${isDealer ? 'text-purple' : 'text-text-muted group-hover:text-primary'}`} />
                        <span className={`ml-2 text-xs font-medium hidden lg:inline ${isDealer ? 'text-purple font-bold' : 'text-text-muted group-hover:text-primary'}`}>
                            {isDealer ? 'ÇIKIŞ YAP' : 'BAYİ GİRİŞİ'}
                        </span>
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
