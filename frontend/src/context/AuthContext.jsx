import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    // Permanent "Demo User" state
    const [user] = useState({
        id: "123e4567-e89b-12d3-a456-426614174000", // Valid UUID for DB compatibility
        email: "demo@medguard.app",
        role: "user",
        created_at: new Date().toISOString()
    });

    const value = {
        user,
        loading: false, // Always ready
        signUp: async () => console.log("SignUp disabled in Demo Mode"),
        signIn: async () => console.log("SignIn disabled in Demo Mode"),
        signOut: async () => {
            if (confirm("Reset Demo Session? (This just refreshes the page)")) {
                window.location.reload();
            }
        },
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
