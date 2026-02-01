"use client";
import React, { createContext, useContext, useState, useEffect } from 'react';

const DealerContext = createContext();

export function DealerProvider({ children }) {
    const [isDealer, setIsDealer] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [isLoginOpen, setIsLoginOpen] = useState(false);

    // Check localStorage on mount
    useEffect(() => {
        const storedStatus = localStorage.getItem('isDealer');
        if (storedStatus === 'true') {
            setIsDealer(true);
        }
        setIsLoading(false);
    }, []);

    const login = (password) => {
        if (password === 'bayi123') {
            setIsDealer(true);
            localStorage.setItem('isDealer', 'true');
            setIsLoginOpen(false); // Close modal on success
            return true;
        }
        return false;
    };

    const logout = () => {
        setIsDealer(false);
        localStorage.removeItem('isDealer');
    };

    // Helper to get price based on role
    const getPrice = (originalPrice) => {
        return isDealer ? 45 : 90;
    };

    return (
        <DealerContext.Provider value={{ isDealer, login, logout, getPrice, isLoading, isLoginOpen, setIsLoginOpen }}>
            {children}
        </DealerContext.Provider>
    );
}

export function useDealer() {
    return useContext(DealerContext);
}
