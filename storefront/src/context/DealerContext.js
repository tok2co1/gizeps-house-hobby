"use client";
import React, { createContext, useContext, useState, useEffect } from 'react';

const DealerContext = createContext();

export function DealerProvider({ children }) {
    const [isDealer, setIsDealer] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

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
        <DealerContext.Provider value={{ isDealer, login, logout, getPrice, isLoading }}>
            {children}
        </DealerContext.Provider>
    );
}

export function useDealer() {
    return useContext(DealerContext);
}
