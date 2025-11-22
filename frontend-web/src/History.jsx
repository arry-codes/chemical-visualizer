import React, { useEffect, useState } from 'react';
import api from './api';

const History = ({ onSelectUpload, refreshTrigger, auth }) => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get('history/', {
                    headers: {
                        'Authorization': `Basic ${btoa(`${auth.username}:${auth.password}`)}`
                    }
                });
                setHistory(response.data);
            } catch (error) {
                console.error('Error fetching history:', error);
            }
        };
        fetchHistory();
    }, [refreshTrigger, auth]);

    return (
        <div className="p-4 bg-white rounded shadow">
            <h3 className="mb-2 text-lg font-bold">Recent Uploads</h3>
            <ul>
                {history.map((item) => (
                    <li
                        key={item.id}
                        onClick={() => onSelectUpload(item.id)}
                        className="p-2 mb-1 cursor-pointer hover:bg-gray-100"
                    >
                        {item.filename} <span className="text-xs text-gray-500">({new Date(item.uploaded_at).toLocaleString()})</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default History;
