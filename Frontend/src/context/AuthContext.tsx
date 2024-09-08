import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { login, logout, isAuthenticated, getUser } from '../lib/authServices'

interface User {
  id: string,
  name: string,
  email: string
}

interface AuthContextData {
  signed: boolean,
  user: User | null,
  signIn(email: string, password: string): Promise<void>,
  signOut(): void
}

const AuthContext = createContext<AuthContextData | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState(getUser());

  useEffect(() => {
    if (isAuthenticated()) {
      setUser(getUser());
    }
  }, []);

  const signIn = async (email: string, password: string) => {
    const data = await login(email, password);
    setUser(data.user);
  };

  const signOut = () => {
    logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ signed: !!user, user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextData {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser utilizado dentro de um AuthProvider');
  }
  return context;
}
