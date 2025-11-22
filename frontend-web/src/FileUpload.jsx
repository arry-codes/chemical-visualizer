import React, { useState } from 'react';
import api from './api';

const FileUpload = ({ onUploadSuccess, auth }) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post('upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Basic ${btoa(`${auth.username}:${auth.password}`)}`
                }
            });
            setMessage('Upload successful!');
            onUploadSuccess(response.data.upload_id);
        } catch (error) {
            setMessage('Upload failed: ' + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div className="p-4 mb-4 bg-white rounded shadow">
            <h3 className="mb-2 text-lg font-bold">Upload CSV</h3>
            <input type="file" onChange={handleFileChange} accept=".csv" className="mb-2" />
            <button
                onClick={handleUpload}
                className="px-4 py-2 font-bold text-white bg-green-500 rounded hover:bg-green-700"
            >
                Upload
            </button>
            {message && <p className="mt-2 text-sm">{message}</p>}
        </div>
    );
};

export default FileUpload;
