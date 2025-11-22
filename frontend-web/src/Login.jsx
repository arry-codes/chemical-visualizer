import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = ({ setAuth }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();

        if (username && password) {
            const authData = { username, password };
            localStorage.setItem('auth', JSON.stringify(authData));
            setAuth(authData);
            navigate('/dashboard');
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="p-8 bg-white rounded shadow-md w-96">
                <h2 className="mb-4 text-2xl font-bold text-center">Login</h2>
                <form onSubmit={handleLogin}>
                    <div className="mb-4">
                        <label className="block mb-2 text-sm font-bold text-gray-700">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-3 py-2 border rounded shadow appearance-none"
                        />
                    </div>
                    <div className="mb-6">
                        <label className="block mb-2 text-sm font-bold text-gray-700">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-3 py-2 border rounded shadow appearance-none"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
